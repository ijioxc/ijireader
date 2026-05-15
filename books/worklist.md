# 📚 書庫數據建置工作清單

#### 📌 Phase 1：經典文學與哲學（來源：Standard Ebooks）— 最優先處理
*處理流程：直接去 Standard Ebooks 載 EPUB -> 丟進 Python 腳本拆成 JSON 資料夾。*
- [ ] **The Picture of Dorian Gray**（格雷的畫像）
- [ ] **The Great Gatsby**（大亨小傳）
- [ ] **1984**
- [ ] **The Adventures of Sherlock Holmes**（福爾摩斯探案集）
- [ ] **Frankenstein**（科學怪人）
- [ ] **Moby-Dick**（白鯨記）
- [ ] **The Book of Tea**（茶之書）
- [ ] **Bushido: The Soul of Japan**（武士道）
- [ ] **Brave New World**（美麗新世界）
- [ ] **Meditations**（沉思錄）
- [ ] **Beyond Good and Evil**（善惡的彼岸）
- [ ] **The Republic**（理想國）
- [ ] **The Prophet**（先知）
- [ ] **The Bible**（聖經 - 文學版）
- [ ] **The Count of Monte Cristo**（基督山恩仇記）
- [ ] **The Three Musketeers**（三劍客）

#### 📌 Phase 2：網路小說（來源：Royal Road / Novel Updates）— 需用工具抓取
*處理流程：用 `WebToEpub` 插件抓網頁 -> 轉成 EPUB -> 丟進 Python 腳本拆成 JSON。*
- [ ] **Mother of Learning**（Royal Road 天花板）
- [ ] **The Wandering Inn**（最長網文天花板）
- [ ] **無職轉生**（從 Novel Updates 找翻譯組連結）
- [ ] **關於我轉生變成史萊姆這檔事**（從 Novel Updates 找翻譯組連結）

#### 📌 Phase 3：其他名著與版權書（來源：圖書館 / 其他電子書站）— 需自行尋找乾淨 EPUB
- [ ] **Howl's Moving Castle**（哈爾移動城堡）
- [ ] **No Longer Human**（人間失格）
- [ ] **The Beast Player**（獸之奏者）
- [ ] **Dune**（沙丘）
- [ ] **The Hitchhiker's Guide to the Galaxy**（銀河便車指南）
- [ ] **The Catcher in the Rye**（麥田捕手）
- [ ] **The Protestant Ethic and the Spirit of Capitalism**（新教倫理與資本主義精神）
- [ ] **Orientalism**（東方主義）

#### 📌 Phase 4：系統整合與黑魔法
- [ ] **架設 TTS 串流後端**：用 FastAPI 寫好 `edge-tts` 的串流 API。
- [ ] **自動化批次處理**：寫一個 Python 迴圈，把下載下來的 EPUB 批次自動轉成 JSON 資料夾。
- [ ] **前端渲染測試**：將 Phase 1 產出的 JSON 餵給 `reader.html`，測試長文本滾動與播放流暢度。



Viewed worklist.md:1-43

**答案：直接給你這段「交接提示詞」，你開新對話時直接複製這段貼給他就行了。**

```markdown
# 專案交接與上下文 (Context)

## 1. 目前進度與背景
- 使用者正在開發一個英文閱讀器（`reader.html`），位於 `/Users/ijioxc/Desktop/英文code/ijieng/`。
- 目標是獲取高品質開源書/網文的 JSON 數據（按章節切分），並整合微軟品質的 TTS 語音播放功能。

## 2. 這輪對話已完成事項
- **TTS 方案**：確定使用 Python `edge-tts`。已提供 FastAPI 串流 MP3 的後端代碼，以及前端 `new Audio()` 的串接方法。
- **數據解析**：已提供 Python 腳本，可將 Standard Ebooks 的 EPUB（ZIP）解壓並將各章節 HTML 轉存為 JSON 資料夾。
- **書庫清單**：已挑選 28 本涵蓋名著、哲學、網文、大學生文青最愛的作品。
- **產出檔案**：
  - 書籍 JSON 陣列已存在 `/Users/ijioxc/Untitled-1.json`。
  - 任務追蹤清單已建立於 `/Users/ijioxc/Desktop/英文code/ijieng/worklist.md`。

## 3. 接下來的任務（請 AI 從這裡接手）
請根據 `worklist.md` 的規劃，協助使用者：
1. 獲取並解析 Standard Ebooks 的 EPUB 檔案（例如先拿《The Great Gatsby》測試）。
2. 實作並運行 Phase 4 的 FastAPI TTS 串流伺服器。
3. 協助調整 `reader.html` 的 UI 與數據對接。
```

---

### 需求重述與詳細說明
你想要一段文字，用來把這次對話的工作進度交接給下一段對話（開新的對話視窗）。

我幫你寫了一份結構非常清晰的「交接上下文」。它明確告訴下一隻 AI 我們的專案路徑、已經解決的 TTS 與數據拆解方案、整理好的書籍清單位置（`Untitled-1.json` 和 `worklist.md`），以及接下來要執行的具體步驟。這樣你可以直接開啟新對話，不用浪費 Token 重新解釋。

---
**來源參考：**
* 本次對話上下文整理