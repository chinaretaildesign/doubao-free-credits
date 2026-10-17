# Play 上传交付包

构建时间：2026-10-17 22:53 · 构建机：本机（I 盘 JDK 21 + SDK 36）

## 文件清单

| 文件 | 用途 | 上传到 Play Console 哪个位置 |
| --- | --- | --- |
| `ChinaTravelAssistant-v1.0-release.aab` | **应用包（必传）** | 测试 → 内部测试 → 创建新版本 → 上传 |
| `ChinaTravelAssistant-v1.0-universal.apk` | 本地装到手机自测用（**不上传 Play**） | — |
| `icon-512.png` | 应用图标 | 商店设置 → 主要商店信息 → 应用图标 |
| `feature-graphic-1024x500.png` | 宣传图片 | 商店设置 → 主要商店信息 → 宣传图片 |
| `screenshots/01~06.png` | 手机截图（6 张，要求 ≥2） | 商店设置 → 主要商店信息 → 手机屏幕截图 |

## 校验数据（2026-10-17 实测）

**AAB**
```
文件名       : ChinaTravelAssistant-v1.0-release.aab
大小         : 7,333,626 字节
SHA-256      : baac116abd1c6bdef6933ea8cd515d73d1c2eef0fb7f0f6e1f7d7f675bf207e6
条目数       : 531
.dex 文件    : 1 个（base/dex/classes.dex）
.so 原生库   : 0 个
签名验证     : jarsigner -verify → exit 0（通过）
```

**签名证书（与交接密钥完全一致）**
```
DN       : CN=ChinaRetailDesign, OU=Mobile, O=ChinaRetailDesign, L=Shanghai, ST=Shanghai, C=CN
SHA-256  : 97:B3:25:E5:0B:2D:61:7C:E8:C0:0F:2B:F1:DA:67:E3:E6:A4:07:73:5C:E6:61:6E:96:26:49:06:32:FF:2D:2B
别名     : china-travel-release（keystore: C:/Users/15051/WorkBuddy/keys/china-travel-release.jks）
```

**应用元信息（aapt2 实测）**
```
包名          : com.chinaretaildesign.assistant
versionCode   : 1
versionName   : 1.0
minSdk        : 24 (Android 7.0)
targetSdk     : 36 (Android 16)
compileSdk    : 36
应用名        : China Travel Assistant
```

**16KB 页对齐（Google Play 2025-11 起强制，2026-07 起对 Android 15+ 应用强制）**
```
zipalign -c -P 16 -v 4 app-release.apk → Verification succesful
且 APK/AAB 内含 0 个 .so 原生库 → 该要求对本应用天然满足
```

**权限**
```
标准权限声明：0 个（uses-permission 为空）
仅系统自动注入 com.chinaretaildesign.assistant.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
→ 无 INTERNET、无定位、无相机、无存储、无通讯录
→ 数据安全表单可全部填「不收集」
```

## 重要：上传前必须做的两件事

### 1. 记录并备份签名的 SHA-256

上面那串 `97:B3:25...FF:2D:2B` 是**应用的身份**。Play 后台、三星后台、任何后续版本都必须用它签名。丢了就无法更新已上架的 App（只能换包名重新发布，等于丢掉所有用户）。

**已备份位置**：
- `C:/Users/15051/WorkBuddy/keys/china-travel-release.jks`（主）
- `I:/Desktop/chinatravelassistant/keys/`（副本）

**建议再做一次离线备份**（U 盘 / 加密云盘），并把这串 SHA-256 抄在本文件里打印出来存着。

### 2. 首次上传时勾选 Play App Signing

Play Console 上传第一个 AAB 时会问：

> **Use Play App Signing?** → 选 **Yes / 继续**

含义：你上传的 AAB 用你的密钥签名（叫「上传密钥」），Google 再用它自己保管的「应用签名密钥」重新签一份分发给用户。

- ✅ 好处：密钥丢了可以找 Google 恢复
- ⚠️ 代价：**从 Play 装的应用签名 ≠ 你本地 APK 的签名**，两者不能互相覆盖安装（详见 `APK-DISTRIBUTION-ANALYSIS.md`）

## 版本号策略（下次改版必看）

`versionCode` 每次上传必须**严格递增**（1 → 2 → 3），`versionName` 是显示给用户看的（1.0 → 1.1）。

改的地方：`android/app/build.gradle`

```gradle
defaultConfig {
    versionCode 2        // ← 每次发布 +1，不能重复，不能回退
    versionName "1.1"    // ← 用户看到的版本号
}
```

## 重新构建命令

```bash
export JAVA_HOME='I:/Desktop/chinatravelassistant/Android/jdk-21'
export PATH="$JAVA_HOME/bin:$PATH"
cd "C:/Users/15051/WorkBuddy/技能开发/china-travel-assistant/android"
./gradlew.bat bundleRelease
```

产物：`android/app/build/outputs/bundle/release/app-release.aab`

若代码有改动（改了 `src/` 或 `public/`），**必须先**重新生成 Web 产物再打包，否则 AAB 里还是旧内容：

```bash
cd "C:/Users/15051/WorkBuddy/技能开发/china-travel-assistant"
npm run build          # vite build + tsc
npx cap sync android   # 把 dist 同步进 android/app/src/main/assets/public
cd android && ./gradlew.bat bundleRelease
```
