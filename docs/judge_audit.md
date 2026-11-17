# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có (`observed=0.28 -> RG=0.30`) | dùng |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không (`observed=0.09 -> RG=0.30`) | loại |

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Người | Xưng "em" + "nha" quá suồng sã với khách. Sửa rubric: cấm đại từ/từ ngữ thân mật (*em/nha/bạn*), yêu cầu xưng *anh/chị*. |
| 2 | H-029 | PASS | FAIL | Người | Giọng ra lệnh ("không cần nhắn thêm") dù mở đầu bằng "Dạ, vui lòng". Sửa rubric: phạt câu chặn/ra lệnh khách bất kể từ đệm lịch sự. |
| 3 | H-042 | FAIL | PASS | Người | Trả lời ngắn gọn, đủ ý; Judge phạt oan vì "thiếu xin lỗi". Sửa rubric: không bắt buộc xin lỗi khi yêu cầu hoàn tiền đã xử lý hợp lệ. |
| 4 | H-051 | FAIL | PASS | Người | Dùng từ "refund" được chính sách CS LogiX cho phép. Sửa rubric: thêm whitelist thuật ngữ tiếng Anh hợp lệ (*refund*). |
| 5 | H-081 | FAIL | PASS | Judge | Nhãn người chấm bị nhầm khi đọc ticket; Judge đúng. Hành động: sửa lại nhãn gốc trong dataset, không sửa rubric. |
| 6 | H-094 | PASS | FAIL | Người | Văn bản dịch máy, mất dấu tiếng Việt (*"Da, LogiX da hoan..."*). Sửa rubric: bắt buộc tiếng Việt có dấu chuẩn. |
| 7 | HL-016 | PASS | FAIL | Người | Văn phong rất dài và xin lỗi nhiều nhưng báo sai số tiền (`55.000đ` vs ledger `35.000đ`). Sửa: loại Judge text-only cho tiêu chí đúng tiền/hữu ích, chuyển sang code grader đọc ledger. |

## Kết luận
- **Tiêu chí bị loại:** `helpful` bị loại hoàn toàn khỏi gate. Ma trận nhầm lẫn `{'tp': 9, 'fp': 0, 'fn': 21, 'tn': 70}` cho thấy tuy `Precision = 1.000`, `Recall` chỉ đạt `0.300` và `κ = 0.375` (dưới ngưỡng `FLOORS`: `κ ≥ 0.6, P ≥ 0.8, R ≥ 0.7`) vì bỏ sót tới `21/30` ca lỗi thật (`observed fail rate 0.09` che giấu `corrected fail rate 0.30`). Nguyên nhân: Judge mắc *verbosity bias* (câu dài, xin lỗi nhiều là cho `PASS`) và không thấy được ledger để phát hiện lỗi sai số tiền (18 ca `sai tiền` + 3 ca `sai xưng hô`).
- **`tone_ok`:** Đạt cả 3 ngưỡng `FLOORS` (`κ = 0.757`, `P = 0.857`, `R = 0.800`; `observed 0.28 -> Rogan–Gladen 0.30`), có thể dùng cho tiêu chí giọng điệu sau khi cập nhật rubric và sửa nhãn `H-081`.
- **Rủi ro còn lại:** Judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có tập held-out thật nhằm xác nhận không bị overfit rubric.
