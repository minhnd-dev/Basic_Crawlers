# Giới thiệu
Đây là một spider đơn giản sử dụng thư viện [Scrapy](https://scrapy.org/) để lấy dữ liệu text từ hơn 10.000 bài báo từ trang báo [Genk](www.genk.vn).  
  Dữ liệu được lấy về được lưu ở file ```OUTPUT/genk-content.json```.  
  Một số thông tin về crawler này:  
  - Số lượng bài báo lấy được: 12937 bài báo  
  - Dữ liệu thu được: Đường link bài báo, tiêu đề, tóm tắt, nội dung, thời gian, nguồn báo, tác giả, tags, chuyên mục  
  - Tốc độ crawl trung bình: ~2500 bài/phút  

# Cách lấy link bài báo
Đầu tiên, em vào trang của của [Genk](https://genk.vn) để lấy link của các bài báo. Tuy nhiên, trang web này không có nút "Xem thêm" để lấy link sang trang tiếp theo mà trang này tự động tải thêm dữ liệu đến vô hạn. Em phát hiện ra mỗi khi kéo đến cuối trang, trang web sẽ gửi request đến địa chỉ https://genk.vn/ajax-home/page-2/20200727153712189__20200725211234502__20200714155940046__20200728113853189__20200728150434174.chn". Trang web này chứa đường dẫn tới các bài báo sẽ xuất hiện sau khi kéo đến cuối trang. Như vậy, em chỉ cần tạo vòng lặp thay thế số page trong địa chỉ kia là có thể lấy được rất nhiều link dẫn đến các bài báo khác nhau.
