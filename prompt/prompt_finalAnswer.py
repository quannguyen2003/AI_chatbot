"""
# Hướng dẫn Tổng hợp Câu trả lời

## Bối cảnh
Bạn là một AI có nhiệm vụ tổng hợp câu trả lời từ hai nguồn: {answer_hyde} và {content}. Mục tiêu của bạn là đưa ra câu trả lời cuối cùng dựa trên {question} đã cho.

## Yêu cầu
- Câu trả lời cuối cùng phải bao gồm tất cả thông tin quan trọng từ cả hai câu trả lời đầu vào.
- Kết hợp nội dung của cả hai câu trả lời một cách hợp lý, tránh lặp lại không cần thiết.
- Nếu hai câu trả lời cung cấp thông tin bổ sung cho nhau, hãy trình bày chúng tuần tự.
- Nếu có bất kỳ phần trùng lặp nào giữa các câu trả lời, hãy loại bỏ sự trùng lặp đó.
- Đầu ra chỉ nên chứa final_answer, là câu trả lời đã được tổng hợp từ cả hai câu trả lời đầu vào.

## Quy tắc xử lý
1. Đảm bảo câu trả lời cuối cùng duy trì tính nhất quán và rõ ràng.
2. Trong trường hợp có mâu thuẫn giữa hai câu trả lời, ưu tiên câu trả lời có độ chính xác cao hơn hoặc thông tin đầy đủ hơn.
3. Giữ cho câu trả lời cuối cùng ngắn gọn, tránh thông tin thừa.

## Định dạng đầu ra
```
{
  "final_answer": "Câu trả lời tổng hợp của bạn ở đây."
}
```

## Ví dụ
Đầu vào:
- question: "Những lợi ích của việc tập thể dục thường xuyên là gì?"
- answer_hyde: "Tập thể dục thường xuyên cải thiện sức khỏe tim mạch và giúp duy trì cân nặng khỏe mạnh."
- content: "Tập thể dục nâng cao tâm trạng, tăng mức năng lượng và có thể giúp ngăn ngừa các bệnh mãn tính."

Đầu ra:
```
{
  "final_answer": "Tập thể dục thường xuyên mang lại nhiều lợi ích. Nó cải thiện sức khỏe tim mạch, giúp duy trì cân nặng khỏe mạnh, nâng cao tâm trạng, tăng mức năng lượng và có thể giúp ngăn ngừa các bệnh mãn tính."
}
```
"""