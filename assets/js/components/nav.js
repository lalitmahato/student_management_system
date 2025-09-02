function profileHover() {
  const dropdown = document.getElementById("profile-hover");
  const imgOutline = document.getElementById("dashboard-nav-profile-img");

  if (dropdown.style.display === "block") {
    dropdown.style.display = "none";
    imgOutline.style.outline = "none";
  } else {
    dropdown.style.display = "block";
    imgOutline.style.outline = "2px solid var(--primary-green)";
  }
}
