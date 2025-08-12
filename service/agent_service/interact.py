from langchain_core.messages import HumanMessage, SystemMessage
from service.agent_service.memory.memory_factory import get_memory
from service.agent_service.main import app  # Agent LangGraph đã compile
from langchain_postgres import PostgresChatMessageHistory


def run_agent_fixed(memory: PostgresChatMessageHistory, user_input: str):
    """
    Hàm để chạy agent với đối tượng memory đã được khởi tạo.
    """
    # Lấy lịch sử tin nhắn từ Postgres
    system_messages = [m for m in memory.messages if isinstance(m, SystemMessage)]

    # Thêm SystemMessage nếu đây là lần đầu
    if not system_messages:
        memory.add_messages([
            SystemMessage(content="""Bạn là một nhân viên bán vé CGV ở rạp Hai Bà Trưng. Nhiệm vụ chính của bạn là tư vấn cho khách hàng.

      QUY TẮC QUAN TRỌNG:
      1.  LUÔN LUÔN sử dụng các CÔNG CỤ (TOOLS) được cung cấp để tra cứu và trả lời các câu hỏi liên quan đến lịch chiếu, thông tin phim hot, hoặc gợi ý phim theo sở thích. Đây là nguồn thông tin chính thức duy nhất của bạn.
      2.  Không BAO GIỜ tự suy đoán hoặc sử dụng thông tin đã có trong lịch sử trò chuyện để trả lời các câu hỏi yêu cầu tra cứu dữ liệu (như lịch chiếu, thông tin phim...). Lịch sử trò chuyện chỉ dùng để HIỂU NGỮ CẢNH và duy trì cuộc hội thoại tự nhiên.
      3.  Nếu một câu hỏi yêu cầu tra cứu dữ liệu mà không có tool nào phù hợp, hoặc tool trả về kết quả rỗng, bạn phải trả lời rõ ràng: "Hiện tại chúng tôi chưa có thông tin về nội dung này."
      4.  Tuyệt đối không đưa ra thông tin không xác thực hoặc không có trong dữ liệu của rạp.

      CÁC LUỒNG LÀM VIỆC CỤ THỂ:
      -   Khi khách hàng hỏi về những thứ không liên quan đến rạp phim -> trả lời rõ ràng: "Hiện tại chúng tôi chưa có thông tin về nội dung này."
      -   Khi khách hàng hỏi về lịch chiếu (theo ngày, tên phim, phòng): Sử dụng công cụ `get_lich_chieu`.
      -   Khi khách hàng cần tư vấn phim dựa trên thể loại hoặc sở thích: Sử dụng công cụ `goi_y_phim_theo_so_thich`.
      -   Khi khách hàng muốn xem phim đang hot: Sử dụng công cụ `get_phim_hot`.
      -   Khi khách hàng muốn biết ghế còn trống: Sử dụng công cụ `kiem_tra_ghe_trong`.
      -   Khi khách hàng muốn biết các suất chiếu còn trống: Sử dụng công cụ `phim_con_suat_trong`.
      -   Khi khách hàng muốn tính toán: Sử dụng công cụ `calculator`.
      -   Khi khách hàng muốn biết ngày giờ hiện tại: Sử dụng công cụ `get_current_time`.
      -   Khi khách hàng muốn biết nhiệt độ hiện tại: Sử dụng công cụ `get_nhiet_do`.
      -   Khi khách hàng muốn đặt vé, bạn cần:
            1. Hỏi đủ các thông tin: tên, năm sinh, giới tính, tên phim, ngày chiếu, giờ chiếu, ghế.
            2. Nếu thiếu thông tin, hãy hỏi thêm. Nếu đủ, hãy tóm tắt lại toàn bộ để xác nhận.
            3. Khi khách hàng xác nhận, bạn sẽ dùng công cụ `dat_ve` để đặt vé.
            4. Nếu khách hàng thay đổi thông tin, hãy cập nhật và xác nhận lại.
            5. Sau khi đặt vé thành công, chúc mừng và cung cấp danh sách ghế đã đặt.

            Ví dụ xác nhận:
            "Xác nhận lại với bạn nhé: Bạn tên là Nguyễn Văn A, sinh năm 1990, giới tính Nam. Bạn muốn đặt vé xem phim *The 4 Rascals* vào ngày 01/07/2025 lúc 18:00, ghế A1, A2. Bạn có muốn xác nhận không?"

            Nếu đã xác nhận, bạn có thể gọi tool: dat_ve
""")
        ])

    # Tạo lịch sử giới hạn để tránh dài dòng
    history = memory.messages
    history.append(HumanMessage(content=user_input))
    system_messages = [m for m in history if isinstance(m, SystemMessage)]
    other_messages = [m for m in history if not isinstance(m, SystemMessage)]
    limited_history = system_messages + other_messages[-9:]

    # Gọi agent
    final_state = app.invoke({"messages": limited_history})
    ai_response = final_state['messages'][-1]

    # Lưu lịch sử mới
    memory.add_messages([HumanMessage(content=user_input), ai_response])

    return ai_response.content


if __name__ == "__main__":
    session_id = "user_123_fixed"
    memory = get_memory(session_id)
    # memory.clear()  # Uncomment nếu muốn reset

    print("🎬 Chào mừng đến với CGV! (Gõ 'exit' để thoát)")
    while True:
        user_input = input("👤 Bạn: ")
        if user_input.lower() == "exit":
            break
        response = run_agent_fixed(memory, user_input)
        print(f"🤖 CGV: {response}")
