import win32com.client
import os

doc_path = os.path.abspath(r"C:\Users\edgeo\.gemini\antigravity\brain\da3b51fe-761e-4b42-b758-d3b8db6abc76\.user_uploaded\media_1793252608778_9f3f34e4.doc")
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
doc = word.Documents.Open(doc_path)

with open("template_dump.txt", "w", encoding="utf-8") as f:
    for i in range(1, doc.Paragraphs.Count + 1):
        f.write(f"P{i}: {doc.Paragraphs(i).Range.Text.strip()}\n")
    for t_idx in range(1, doc.Tables.Count + 1):
        tbl = doc.Tables(t_idx)
        f.write(f"\n=== TABLE {t_idx} (rows: {tbl.Rows.Count}, cols: {tbl.Columns.Count}) ===\n")
        for r in range(1, tbl.Rows.Count + 1):
            row_texts = []
            for c in range(1, tbl.Columns.Count + 1):
                try:
                    cell_txt = tbl.Cell(r, c).Range.Text.strip().replace("\r", "").replace("\x07", "")
                    row_texts.append(cell_txt)
                except Exception:
                    row_texts.append("N/A")
            f.write(f"  Row {r}: {' | '.join(row_texts)}\n")

doc.Close()
word.Quit()
print("Dumped template successfully")

