/**
 * AlumniConnect — University SaaS Frontend JavaScript Controller
 */

// Mobile Sidebar Drawer Controller
function toggleMobileSidebar() {
  const sidebar = document.getElementById('mobile-sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  if (sidebar && overlay) {
    sidebar.classList.toggle('-translate-x-full');
    overlay.classList.toggle('hidden');
  }
}

// Password Visibility Toggle
function togglePassword(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  if (input && icon) {
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    } else {
      input.type = 'password';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  }
}

// Role Tabs in Register / Login
function selectRole(roleName) {
  const roleInput = document.getElementById('role');
  if (roleInput) roleInput.value = roleName;

  document.querySelectorAll('.role-tab-btn').forEach(btn => {
    if (btn.dataset.role === roleName) {
      btn.classList.add('bg-white', 'shadow-xs', 'text-blue-600', 'font-bold');
      btn.classList.remove('text-slate-500');
    } else {
      btn.classList.remove('bg-white', 'shadow-xs', 'text-blue-600', 'font-bold');
      btn.classList.add('text-slate-500');
    }
  });

  const studentFields = document.getElementById('student-fields');
  const alumniFields = document.getElementById('alumni-fields');

  if (studentFields && alumniFields) {
    if (roleName === 'student') {
      studentFields.classList.remove('hidden');
      alumniFields.classList.add('hidden');
    } else {
      studentFields.classList.add('hidden');
      alumniFields.classList.remove('hidden');
    }
  }
}

// Demo Login Autofill Helper
function fillDemo(email, pass) {
  const emailIn = document.getElementById('email');
  const passIn = document.getElementById('password');
  if (emailIn) emailIn.value = email;
  if (passIn) passIn.value = pass;
}

// Modal Helpers
function openModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove('hidden');
}

function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.add('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alerts after 5s
  setTimeout(() => {
    document.querySelectorAll('.flash-alert').forEach(el => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.5s ease';
      setTimeout(() => el.remove(), 500);
    });
  }, 5000);
});
