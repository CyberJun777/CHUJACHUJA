import com.android.apksig.ApkSigner;
import com.android.apksig.ApkVerifier;
import java.io.File;
import java.io.FileInputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.X509Certificate;
import java.util.Collections;

public class Sign {
    public static void main(String[] a) throws Exception {
        KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
        try (FileInputStream in = new FileInputStream(a[0])) { ks.load(in, "android".toCharArray()); }
        PrivateKey key = (PrivateKey) ks.getKey("demo", "android".toCharArray());
        X509Certificate cert = (X509Certificate) ks.getCertificate("demo");
        ApkSigner.SignerConfig sc = new ApkSigner.SignerConfig.Builder("demo", key, Collections.singletonList(cert)).build();
        new ApkSigner.Builder(Collections.singletonList(sc))
            .setInputApk(new File(a[1])).setOutputApk(new File(a[2]))
            .setV1SigningEnabled(false).setV2SigningEnabled(true).setMinSdkVersion(24).build().sign();
        ApkVerifier.Result r = new ApkVerifier.Builder(new File(a[2])).setMinCheckedPlatformVersion(24).build().verify();
        System.out.println("verified=" + r.isVerified() + " v1=" + r.isVerifiedUsingV1Scheme() + " v2=" + r.isVerifiedUsingV2Scheme());
        for (Object e : r.getErrors()) System.out.println("ERROR " + e);
        if (!r.isVerified()) System.exit(1);
    }
}
