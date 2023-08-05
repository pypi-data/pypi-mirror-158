_D='kinesis'
_C='moto'
_B=None
_A='localstack'
import inspect,logging,os
from typing import Any,Dict,List,Optional,Set,Type,Union
import localstack.config as localstack_config,moto.core
from localstack.constants import AWS_REGION_US_EAST_1,TEST_AWS_ACCOUNT_ID
from localstack.services.generic_proxy import RegionBackend
from localstack.services.plugins import BackendStateLifecycle
from localstack.utils.aws.aws_stack import get_valid_regions_for_service
from localstack.utils.files import cp_r,rm_rf
from localstack.utils.persistence import is_persistence_enabled
from moto.applicationautoscaling.models import ApplicationAutoscalingBackend
from moto.autoscaling.models import AutoScalingBackend
from moto.core.utils import BackendDict
from moto.redshift.models import RedshiftBackend
from moto.s3.models import S3Backend
from localstack_ext.bootstrap.pods.servicestate.service_state import ServiceState
from localstack_ext.bootstrap.pods.servicestate.service_state_types import AccountRegion,AssetByNameType,AssetNameType,AssetValueType,BackendState,ServiceKey
from localstack_ext.bootstrap.state_utils import get_object_dict
from localstack_ext.utils.lookup_utils import get_backend_state
SERVICES_WITHOUT_STATE=['apigatewaymanagementapi','azure','azure','cloudsearch','cloudwatch','configservice','docdb','elasticsearch','iot-data','iot-jobs-data','iotanalytics','iotevents','iotevents-data','iotwireless','mediaconvert','mediastore-data','neptune','qldb-session','rds-data','redshift-data','resource-groups','resourcegroupstaggingapi','route53resolver','s3control','sagemaker-runtime','ssm','swf','timestream-query','timestream-write']
EXTERNAL_SERVICES=['dynamodb',_D,'stepfunctions']
NON_SERVICE_APIS=['edge','support','logs']
LOG=logging.getLogger(__name__)
def retry_load(func):
	def A(*C,**D):
		import time;B,E=0,10;A=b''
		while B<E or len(A)==0:
			A=func(*(C),**D)
			if len(A)>0:return A
			time.sleep(1);B+=1
		return A
	return A
def is_backend_empty(backend,service):
	B=backend
	match service:
		case'lambda':
			for (C,A) in B.regions().items():
				if hasattr(A,'lambdas')and A.lambdas or hasattr(A,'layers')and A.layers:return False
			return True
		case _:return not getattr(B,'REGIONS',{})
def _service_state_from_region_backend(service_backend,api):
	A=service_backend;from localstack_ext.constants import REGION_STATE_FILE as C
	if is_backend_empty(A,api):return ServiceState()
	B=ServiceState()
	for (D,E) in A.regions().items():F=ServiceKey(account_id=TEST_AWS_ACCOUNT_ID,region=D,service=api);G=BackendState(F,{C:E});B.put_backend(G)
	return B
def _service_state_from_backend_state(service_backend,api):
	A=service_backend;from localstack.constants import TEST_AWS_ACCOUNT_ID as C;from localstack_ext.constants import MOTO_BACKEND_STATE_FILE as D;from localstack_ext.services.s3.s3_extended import REGION_PLACEHOLDER as E;B=ServiceState()
	if not isinstance(A,dict):
		if isinstance(A,moto.s3.models.S3Backend):
			if not A.buckets:return B
		A={E:A}
	for (F,G) in A.items():H=ServiceKey(account_id=C,region=F,service=api);I=BackendState(H,{D:G});B.put_backend(I)
	return B
def _service_state_from_backend(backend,api,memory_management):
	B=memory_management;A=backend
	if B==_A:return _service_state_from_region_backend(service_backend=A,api=api)
	if B==_C:return _service_state_from_backend_state(service_backend=A,api=api)
class BackendStateLifecycleBase(BackendStateLifecycle):
	service:0
	def get_backends(D):
		A={}
		for B in [_C,_A]:
			C=get_backend_state(api=D.service,memory_manager=B)
			if C:A[B]=C
		return A
	def retrieve_state(A,**F):
		B=ServiceState();E=A.service;C=A.get_backends()
		for D in C.keys():B.put_service_state(_service_state_from_backend(backend=C[D],api=E,memory_management=D))
		return B
	def inject_state(N,**H):
		G='backend_state';from localstack_ext.services.s3.s3_extended import REGION_PLACEHOLDER as I;J=H.get('backends')
		for B in J:
			K=B.key.region or _B;L=[_C if A==G else _A for A in B.backends.keys()]
			for E in L:
				A=get_backend_state(api=B.key.service,memory_manager=E,region=K);C=_B
				try:C=A[I]
				except Exception:pass
				if C and isinstance(A,dict):A=C
				D=B.backends['region_state'if E==_A else G]
				if isinstance(A,list):A.clear();A.extend(D)
				elif isinstance(A,set):A.clear();A.update(D)
				else:F=get_object_dict(A);M=get_object_dict(D);F.clear();F.update(M)
	def reset_state(B):
		LOG.debug('Resetting state for %s',B.service);D=get_backend_state(B.service,_C);E=get_backend_state(B.service,_A);C=[];D and C.append(D);E and C.append(E)
		if not C:
			if B.service not in SERVICES_WITHOUT_STATE+EXTERNAL_SERVICES+NON_SERVICE_APIS:LOG.debug("Unable to determine state container for service '%s'",B.service)
			return
		for A in C:
			if inspect.isclass(A)and issubclass(A,RegionBackend):A.reset();continue
			if isinstance(A,dict):
				for G in A.keys():reset_moto_backend_state(A,G)
				if isinstance(A,moto.core.utils.BackendDict):A.clear()
				continue
			if isinstance(A,moto.core.BaseBackend):F=getattr(A,'region_name',getattr(A,'region',_B));A.__dict__={};A.__init__(*([F]if F else[]));continue
			LOG.warning("Unable to reset state for service '%s', state container: %s",B.service,A)
		B.on_after_reset()
	def active_service_regions(D):
		def B(reg):return AccountRegion(account_id=TEST_AWS_ACCOUNT_ID,region=reg)
		E=D.get_backends()
		if not E:F=get_valid_regions_for_service(D.service);return set([B(A)for A in F])
		C=set()
		for (G,A) in E.items():
			if inspect.isclass(A)and issubclass(A,RegionBackend):C.update(set([B(C)for C in A.regions().keys()]))
			elif isinstance(A,dict):C.update(set([B(C)for C in A.keys()]))
			elif isinstance(A,S3Backend):return{B(AWS_REGION_US_EAST_1)}
			else:return{B('global')}
		return C
	def on_after_reset(A):0
class BackendStateAssetsLifecycle(BackendStateLifecycleBase):
	def assets_root(A):return A.service
	def get_assets_location(A):B=localstack_config.dirs.data if is_persistence_enabled()else localstack_config.dirs.tmp;return os.path.join(B,A.assets_root())
	def retrieve_assets(C,**H):
		A=C.get_assets_location();B={}
		if not os.path.isdir(A):return B
		for D in os.listdir(A):
			E=os.path.join(A,D)
			if os.path.isfile(E):F=D;G=C._load_asset(E);B[F]=G
		return B
	@retry_load
	def _load_asset(self,path):return self._load_asset_binary(path)
	@staticmethod
	def _load_asset_binary(file_path):
		A=file_path
		try:
			with open(A,'rb')as B:return B.read()
		except Exception as C:LOG.warning(f"Could not load assets binary for file {A} due to {C}.");return _B
	def inject_assets(A,pod_assets_dir):B=A.get_assets_location();C=os.path.join(pod_assets_dir,A.assets_root());rm_rf(B);cp_r(C,B)
	def retrieve_state(B,**C):
		A=super().retrieve_state(**C)
		if not A.state and B.service!=_D:return A
		D=B.retrieve_assets();A.put_assets(B.service,D);return A
	def inject_state(B,**A):super().inject_state(**A)
	def reset_state(A):B=A.get_assets_location();rm_rf(B);super().reset_state()
def reset_moto_backend_state(state_container,region_key):
	D=state_container;B=region_key;A=D.get(B);E=getattr(A,'reset',_B)
	if E and callable(E):E();return A
	F=type(A);C=[B]if len(inspect.signature(F.__init__).parameters)>1 else[]
	if isinstance(A,ApplicationAutoscalingBackend):C.append(A.ecs_backend)
	elif isinstance(A,RedshiftBackend):C.insert(0,A.ec2_backend)
	elif isinstance(A,AutoScalingBackend):C=[A.ec2_backend,A.elb_backend,A.elbv2_backend]
	D[B]=F(*(C));return D[B]
class DummyProvider(BackendStateLifecycleBase):
	def __init__(A,service):A.service=service