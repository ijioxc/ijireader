# Reader — Bilingual 架構規範指南 (AI 檢修專用)

## 📌 核心設計原則
1. **單一檔案架構**：所有邏輯、樣式與結構皆在 `reader.html` 中，修改時需注意全域變數與函數的命名衝突。
2. **語音優先**：本系統核心為雙語朗讀與翻譯，任何 UI 異動皆需考量是否影響 `speechSynthesis` 播放。

## 💾 狀態管理 (LocalStorage)
AI 在新增或讀取設定時，必須嚴格遵守以下 Key 值規範：
*   `gemini_api_key`: Gemini API 密鑰。
*   `deepl_api_key`: DeepL API 密鑰。
*   `translation_engine`: 目前使用的翻譯引擎 (`gemini` 或 `deepl`)。
*   `display_order`: 語系順序 (`en` 或 `zh`)。**嚴禁使用 `displayOrder`**。
*   `selectedTheme`: 目前主題。
*   `fontSize`: 字體大小。
*   `selectedFont`: 英文字體。
*   `selectedZhFont`: 中文字體。

## 🛠 關鍵函數與防呆機制
*   `checkProxyOnce()`: 翻譯前必須呼叫，檢查 CORS 代理是否存活（檢查 status 是否 < 500）。
*   `callTranslate()`: 統一翻譯入口，內含代理檢查。
*   `loadVoices()`: 語音清單載入，內含 3 秒超時防護，避免選單卡在「正在載入語音...」。
*   `setOrder(order)`: 統一更新語系順序的入口，會同時更新 UI 按鈕狀態與 `localStorage`，**不進行頁面重載 (No Reload)**。

## 🎨 UI 綁定規範
*   大部分切換按鈕（主題、字體、順序）皆透過 `setupTabs(containerId, storageKey, applyFn)` 進行綁定。
*   按鈕元素需提供 `data-theme`, `data-size`, `data-font`, 或 `data-order` 作為值。若皆無，則預設讀取 `textContent`。
