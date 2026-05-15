# 電子書與語音處理備忘錄 (Memo)

這個備忘錄記錄了如何將一本開源英文書籍處理並整合至 `reader.html` 閱讀器的完整流程，供後續對話或新任務參考。

---

## 核心流程

### 1. 獲取與清洗全文
*   **來源**：從開源網站或使用者提供的快取中獲取全文。
*   **清洗**：如果檔案帶有行號（例如 `123: Text`），需使用正則表達式 `^\d+: ` 移除行號，確保文本乾淨。
*   **合併**：若分段獲取，需按順序合併為一個完整的 Markdown 或文字檔（如 `book_full.md`）。

### 2. 章節切分
*   **分析**：找出各章節的特徵（例如 Chapter 1, 或者特定的起始句）。
*   **切分**：寫腳本讀取全文，根據特徵將內容切分成獨立的章節區塊。

### 3. 格式化為閱讀器規格 (JSON)
閱讀器預期每本書有一個獨立資料夾，結構如下：
```text
books/
  └── [book_id]/
      ├── manifest.json
      └── chapters/
          ├── 0001.json
          ├── 0002.json
          └── ...
```

#### `manifest.json` 格式：
```json
{
  "title": "書本完整名稱",
  "chapters": [
    {
      "id": 1,
      "title": "Chapter 1 - 標題",
      "url": "chapters/0001.json"
    }
  ]
}
```

#### `chapters/000X.json` 格式：
```json
{
  "id": 1,
  "title": "Chapter 1",
  "content_en": "第一段內容...\n\n第二段內容...\n\n...",
  "content_zh": ""
}
```
> **注意**：`content_en` 必須是單一字串，段落之間用 `\n` 或 `\n\n` 分隔。

### 4. 語音生成 (TTS)
*   **離線方案 (Mac)**：使用 `say` 指令生成 `.m4a` 檔案。
    ```bash
    say -v Samantha -f input.txt -o output.m4a --data-format=aac
    ```
    音訊檔應命名為 `0001.m4a` 並放在 `chapters/` 資料夾下，與 JSON 對齊。
*   **高品質方案 (Edge TTS)**：提供 `edge_tts_gen.py` 腳本，讓使用者在有網路的環境執行，生成微軟品質的 MP3。

---

## 下一步待辦 (Next Steps)
1.  使用者決定下一本要處理的書。
2.  重複上述流程：抓取 -> 清洗 -> 切分 -> 格式化 -> 生成語音。
