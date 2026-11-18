package kr.sinyang.sori;

import android.app.Activity;
import android.content.Intent;
import android.Manifest;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.webkit.GeolocationPermissions;
import android.webkit.WebChromeClient;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** 앱에 담긴 화면(assets/index.html)을 보여 주는 껍데기. 화면 안의 스크립트가 깃허브에서 그날 자료를 받아 온다. */
public class MainActivity extends Activity {
    private WebView web;
    private String geoOrigin;
    private GeolocationPermissions.Callback geoCallback;

    @Override
    protected void onCreate(Bundle saved) {
        super.onCreate(saved);
        web = new WebView(this);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setTextZoom(100);
        // 앱 밖의 웹 주소(비짓제주 등)는 휴대폰 브라우저로 연다. 앱 화면은 그대로 남는다.
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                if (url.startsWith("http://") || url.startsWith("https://")) {
                    try {
                        startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
                    } catch (Exception e) {
                        return false;
                    }
                    return true;
                }
                return false;
            }
        });
        // "내 위치": 화면 안 동의 카드에서 동의한 뒤에만 불린다. 여기서 안드로이드 위치 권한을 한 번 더 묻는다.
        s.setGeolocationEnabled(true);
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
                if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
                        || checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                    callback.invoke(origin, true, false);
                } else {
                    geoOrigin = origin;
                    geoCallback = callback;
                    requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION,
                            Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
                }
            }
        });
        web.setOverScrollMode(WebView.OVER_SCROLL_NEVER);
        setContentView(web);
        if (saved != null) {
            web.restoreState(saved);
        } else {
            web.loadUrl("file:///android_asset/index.html");
        }
    }

    @Override
    public void onRequestPermissionsResult(int code, String[] perms, int[] results) {
        super.onRequestPermissionsResult(code, perms, results);
        if (code != 1 || geoCallback == null) return;
        boolean ok = false;
        for (int r : results) if (r == PackageManager.PERMISSION_GRANTED) ok = true;
        geoCallback.invoke(geoOrigin, ok, false);
        geoCallback = null;
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        web.saveState(out);
    }

    @Override
    public void onBackPressed() {
        if (web.canGoBack()) {
            web.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
        web.evaluateJavascript("window.__liveCheck&&window.__liveCheck()", null);
    }
}
