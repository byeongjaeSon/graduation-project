package ac.kr.hanyang.kiadaservicecountoperator.cr;

public class KiadaServiceCountStatus {
    private boolean ready;

    public boolean isReady() {
        return ready;
    }

    public void setReady(boolean ready) {
        this.ready = ready;
    }

    @Override
    public String toString() {
        return "ElevenStAppStatus{" +
            "ready=" + ready +
            '}';
    }
}

