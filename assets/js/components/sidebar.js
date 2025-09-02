document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('sidebar');
  const sideArrow = document.getElementById('side-arrow');
  const mobileMenuBtn = document.getElementById('mobile__menu-button');
  const mobileCloseBtn = document.getElementById('mobile__close-button');
  const iconLinks = document.querySelectorAll('.icon-link');

  function setInitialSidebarState() {
    const isMobile = window.innerWidth <= 768;

    if (isMobile) {
      sidebar.classList.remove('small');
      sidebar.classList.remove('open');
      sideArrow.style.display = 'none';
      mobileMenuBtn.style.display = 'block';
      mobileCloseBtn.style.display = 'none';
    } else {
      sidebar.classList.remove('open');
      sidebar.classList.remove('small');
      sideArrow.style.display = 'flex';
      mobileMenuBtn.style.display = 'none';
      mobileCloseBtn.style.display = 'none';
    }
  }

  function collapseAllSubmenus() {
    document.querySelectorAll('.sub-menu.collapse.show').forEach(el => {
      bootstrap.Collapse.getOrCreateInstance(el).hide();
    });
  }

  function updateArrowDirection() {
    const icon = sideArrow.querySelector('i');
    if (sidebar.classList.contains('small')) {
      icon.classList.replace('bx-chevron-left', 'bx-chevron-right');
    } else {
      icon.classList.replace('bx-chevron-right', 'bx-chevron-left');
    }
  }

  // Desktop arrow toggle
  sideArrow.addEventListener('click', () => {
    sidebar.classList.toggle('small');
    updateArrowDirection();

    if (sidebar.classList.contains('small')) {
      collapseAllSubmenus();
    }
  });

  // Mobile menu open
  mobileMenuBtn.addEventListener('click', () => {
    sidebar.classList.add('open');
    mobileMenuBtn.style.display = 'none';
    mobileCloseBtn.style.display = 'block';
  });

  // Mobile menu close
  mobileCloseBtn.addEventListener('click', () => {
    sidebar.classList.remove('open');
    mobileCloseBtn.style.display = 'none';
    mobileMenuBtn.style.display = 'block';
  });

  // Prevent Bootstrap Collapse toggle when sidebar is small on desktop
  document.querySelectorAll('.sub-menu.collapse').forEach(collapseEl => {
    collapseEl.addEventListener('show.bs.collapse', function (e) {
      const isSmallSidebar = sidebar.classList.contains('small') && window.innerWidth > 768;
      if (isSmallSidebar) {
        e.preventDefault(); // stop collapse from opening
      }
    });
  });

  // Prevent dummy # links from navigating
  document.querySelectorAll('a[href="#"]').forEach(link => {
    link.addEventListener('click', e => e.preventDefault());
  });

  // On resize
  window.addEventListener('resize', () => {
    setInitialSidebarState();
    updateArrowDirection();

    if (window.innerWidth > 768 && sidebar.classList.contains('small')) {
      collapseAllSubmenus();
    }
  });

  // Initial setup
  setInitialSidebarState();
  updateArrowDirection();
});
