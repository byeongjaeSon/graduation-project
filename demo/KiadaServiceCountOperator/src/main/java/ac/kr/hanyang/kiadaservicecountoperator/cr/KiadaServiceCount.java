package ac.kr.hanyang.kiadaservicecountoperator.cr;

import io.fabric8.kubernetes.api.model.Namespaced;
import io.fabric8.kubernetes.client.CustomResource;
import io.fabric8.kubernetes.model.annotation.Group;
import io.fabric8.kubernetes.model.annotation.Version;

@Version("v1")
@Group("hanyang.ac.kr")
public class KiadaServiceCount extends CustomResource<KiadaServiceCountSpec, KiadaServiceCountStatus> implements Namespaced {
}

