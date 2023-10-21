package ac.kr.hanyang.kiadaservicecountoperator.reconciler;

import ac.kr.hanyang.kiadaservicecountoperator.cr.KiadaServiceCount;
import ac.kr.hanyang.kiadaservicecountoperator.cr.KiadaServiceCountStatus;
import io.fabric8.kubernetes.client.KubernetesClient;
import io.javaoperatorsdk.operator.api.reconciler.Context;
import io.javaoperatorsdk.operator.api.reconciler.ControllerConfiguration;
import io.javaoperatorsdk.operator.api.reconciler.Reconciler;
import io.javaoperatorsdk.operator.api.reconciler.UpdateControl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@ControllerConfiguration
public class KiadaServiceCountReconciler implements Reconciler<KiadaServiceCount>{

    private static final String targetDeploymentName = "kiada";

    private static final String targetNamespace = "default";

    private static final Logger logger = LoggerFactory.getLogger(KiadaServiceCountReconciler.class);
    private final KubernetesClient kubernetesClient;

    public KiadaServiceCountReconciler(KubernetesClient kubernetesClient) {
        this.kubernetesClient = kubernetesClient;
    }

    @Override
    public UpdateControl<KiadaServiceCount> reconcile(KiadaServiceCount resource, Context<KiadaServiceCount> context) {

        // CR 내용 로깅
        logger.info("Start Reconcile Logic!");
        logger.info("CRD name : " + resource.getCRDName());
        logger.info("metadata.name : " + resource.getMetadata().getName());
        logger.info("spec.owner : " +resource.getSpec().getOwner());
        logger.info("spec.kiadaServiceCount : " +resource.getSpec().getKiadaServiceCount());


        // kiada pod 수 오토 스케일링
        kubernetesClient.apps()
            .deployments()
            .inNamespace(targetNamespace)
            .withName(targetDeploymentName)
            .scale(resource.getSpec().getKiadaServiceCount());


        // status 변경
        var status = new KiadaServiceCountStatus();
        status.setReady(true);
        resource.setStatus(status);

        return UpdateControl.patchStatus(resource);
    }
}
