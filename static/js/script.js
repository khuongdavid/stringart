// Thiết lập thời gian hiển thị cho div
$(document).ready(function () {
  setTimeout(function () {
    $('#alert-success').fadeOut('slow') // Ẩn div sau 3 giây
  }, 3000) // 3000ms = 3 giây
})

document.addEventListener('DOMContentLoaded', function () {
  const oldPasswordInput = document.getElementById('oldpassword');
  const submitBtn = document.getElementById('submitBtn');

  oldPasswordInput.addEventListener('input', function () {
    if (this.value.trim() !== '') {
      submitBtn.classList.remove('disabled');
    } else {
      submitBtn.classList.add('disabled');
    }
  });
});

// Lắng nghe sự kiện cuộn trang
// window.addEventListener('scroll', function () {
//   var navbar = document.querySelector('#navbar');

//   // Tính toán giá trị opacity dựa trên vị trí cuộn của trang
//   var opacity = 1 - (window.scrollY / 50); // 50 là một giá trị ngưỡng

//   // Giới hạn giá trị opacity trong khoảng từ 0 đến 1
//   opacity = Math.min(Math.max(opacity, 0), 1);

//   // Áp dụng giá trị opacity vào navbar
//   navbar.style.opacity = opacity.toFixed(2); // Làm tròn giá trị opacity đến 2 chữ số thập phân

//   // Kiểm tra nếu opacity gần bằng 0, ẩn navbar
//   if (opacity < 0.01) {
//     navbar.style.display = 'none';
//   } else {
//     navbar.style.display = ''; // Sử dụng giá trị mặc định của CSS để hiển thị navbar
//   }
// });


// document.addEventListener('DOMContentLoaded', function() {
//   const fileInput = document.getElementById('fileInput');

//   fileInput.addEventListener('change', function() {
//       if (fileInput.files.length > 0) {
//           const fileName = fileInput.files[0].name;
//           const fileExtension = fileName.split('.').pop(); // Lấy phần mở rộng của file
//           const newTitle = 'Ảnh được chọn: ' + fileName; // Tạo tiêu đề mới

//           // Cập nhật tiêu đề của input file
//           fileInput.setAttribute('title', newTitle);
//       }
//   });
// });


