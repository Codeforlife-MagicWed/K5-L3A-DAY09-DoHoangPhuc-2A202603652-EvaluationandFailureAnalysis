# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID `E-seeded_regression-20261117-d926` |
| Triệu chứng | `TrialPass`, `RefundAmountCorrect` và `DbFactKept` FAIL (`status=resolved != denied`); step 6 `reply` nói `"Dạ, LogiX đã hoàn 20.000đ cho đơn O-202."`, ledger ghi `refund_vnd=20000`, `refund_count=1` (đáp án `0`) |
| Bước sai đầu tiên | Event `3` `model_override` `{"delay_days": 5}` |
| Vì sao là bước *đầu tiên* | Event `1` (`handoff`) giao đúng danh sách tool read-only; Event `2` (`investigator`) đọc đúng đơn `O-202` từ DB với `delay_days=2`, `visible=true` — tới Event `3` mới lấy `5` ngày trong ticket ghi đè lên DB |
| Failure mode | `FM-03` (`ticket_trust — tin ticket hơn DB`) |
| Đối chứng | Trên `fixed C-002@11`: không có `model_override`; sau Event `2` (`investigator`) sang thẳng Event `3` (`quote`: `amount_vnd=0`, `no_entitlement`) và Event `4` (`reply` từ chối), `ledger=0`, `status=denied` (`PASS`) |
| Regression test | `tests/test_lab9_regression.py::test_c002_ticket_trust_regression_and_fixed_control` (dùng `DbFactKept` và `RefundAmountCorrect`); đã chạy xác nhận bắt lỗi trên `seeded_regression` và pass trên `fixed` |
| Chưa chắc chắn | Trace chạy bằng `MockLLM` và công tắc gài lỗi; chưa đo được xác suất bị prompt đánh lừa trên LLM thật, và nếu lỗi không phát event `model_override` (`quiet_override`) thì `DbFactKept` đơn lẻ sẽ không bắt được |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
