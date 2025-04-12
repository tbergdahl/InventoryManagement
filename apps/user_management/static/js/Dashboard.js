// Sidebar hover
let list = document.querySelectorAll(".navigation ul li");

function activeLink() {
  list.forEach(item => item.classList.remove("hovered"));
  this.classList.add("hovered");
}
list.forEach(item => item.addEventListener("mouseover", activeLink));

// Sidebar toggle functionality
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

// Chart Tab Switching Functionality with Cache Busting
function showTab(event, id) {
  const tabs = document.querySelectorAll('.chart-content');
  const buttons = document.querySelectorAll('.tab-btn');

  // Hide all chart sections and deactivate all tab buttons
  tabs.forEach(tab => tab.classList.remove('active'));
  buttons.forEach(btn => btn.classList.remove('active'));

  // Show the selected tab
  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');

    // Refresh based on range selector
    const range = document.getElementById(`${id}Range`).value;
    updateChart(id, range);
  }

  // Activate the clicked tab button
  if (event?.target) {
    event.target.classList.add('active');
  }
}

// Dropdown handler inside tabs
function updateChart(chartType, customRange = null) {
  const range = customRange || document.getElementById(`${chartType}Range`).value;
  const img = document.getElementById(`${chartType}-img`);
  const urlMap = {
    pie: {
      daily: "/inventory/charts/daily/pie/",
      weekly: "/inventory/charts/weekly/pie/",
      monthly: "/inventory/charts/monthly/pie/"
    },
    histogram: {
      daily: "/inventory/charts/daily/histogram/",
      weekly: "/inventory/charts/weekly/histogram/",
      monthly: "/inventory/charts/monthly/histogram/"
    },
    line: {
      daily: "/inventory/charts/daily/line/",
      weekly: "/inventory/charts/weekly/line/",
      monthly: "/inventory/charts/monthly/line/"
    },
    bar: {
      daily: "/inventory/charts/daily/bar/",
      weekly: "/inventory/charts/weekly/bar/",
      monthly: "/inventory/charts/monthly/bar/"
    }
  };
  
  if (img && urlMap[chartType] && urlMap[chartType][range]) {
    img.src = `${urlMap[chartType][range]}?t=${Date.now()}`;
  }
}  
