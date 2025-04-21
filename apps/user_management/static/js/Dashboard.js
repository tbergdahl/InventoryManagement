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

if (toggle) {
  toggle.onclick = function () {
    navigation.classList.toggle("active");
    main.classList.toggle("active");
  };
}

// Chart Tab Switching with Cache Busting
function showTab(event, id) {
  const tabs = document.querySelectorAll(".chart-content");
  const buttons = document.querySelectorAll(".tab-btn");

  tabs.forEach(tab => tab.classList.remove("active"));
  buttons.forEach(btn => btn.classList.remove("active"));

  const target = document.getElementById(id);
  if (target) {
    target.classList.add("active");
    const range = document.getElementById(`${id}Range`)?.value;
    updateChart(id, range);

    if (id === 'productwise') {
      updateProductChart(); // auto trigger when switching to productwise
    }
  }

  if (event?.target) {
    event.target.classList.add("active");
  }
}

function updateChart(chartType, customRange = null) {
  const range = customRange || document.getElementById(`${chartType}Range`)?.value;
  const product = document.getElementById("productSelect")?.value || "";
  const timestamp = Date.now();

  const urlMap = {
    pie: {
      weekly: "/inventory/charts/weekly/pie/",
      monthly: "/inventory/charts/monthly/pie/"
    },
    histogram: {
      weekly: "/inventory/charts/weekly/histogram/",
      monthly: "/inventory/charts/monthly/histogram/"
    },
    line: {
      weekly: "/inventory/charts/weekly/line/",
      monthly: "/inventory/charts/monthly/line/"
    },
    bar: {
      weekly: "/inventory/charts/weekly/bar/",
      monthly: "/inventory/charts/monthly/bar/"
    },
    product_line: "/inventory/charts/product/line/",
    product_histogram: "/inventory/charts/product/histogram/"
  };

  if (chartType.startsWith("product_")) {
    const imgId = chartType === "product_line" ? "product-line-img" : "product-histogram-img";
    const img = document.getElementById(imgId);
    const chartUrl = `${urlMap[chartType]}?product=${encodeURIComponent(product)}&t=${timestamp}`;
    if (img) {
      img.src = chartUrl;
      img.style.display = "block";
    }

    const otherImgId = chartType === "product_line" ? "product-histogram-img" : "product-line-img";
    const otherImg = document.getElementById(otherImgId);
    if (otherImg) {
      otherImg.style.display = "none";
    }

  } else {
    const img = document.getElementById(`${chartType}-img`);
    if (img && urlMap[chartType] && urlMap[chartType][range]) {
      img.src = `${urlMap[chartType][range]}?t=${timestamp}`;
    }
  }
}

// Auto update product chart on tab load or dropdown change
function updateProductChart(chartType = null) {
  const selectedChart = chartType || document.querySelector(".product-tab.active")?.dataset.chart || "line";
  updateChart(`product_${selectedChart}`);
}

// Product-wise tab buttons
function switchProductChart(type) {
  const buttons = document.querySelectorAll(".product-tab");
  buttons.forEach(btn => btn.classList.remove("active"));
  document.querySelector(`.product-tab[data-chart='${type}']`)?.classList.add("active");
  updateProductChart(type);
}

// Register product chart events
document.addEventListener("DOMContentLoaded", () => {
  const productSelect = document.getElementById("productSelect");
  if (productSelect) {
    productSelect.addEventListener("change", () => updateProductChart());
  }

  // Trigger default tab on load
  const activeTab = document.querySelector(".tab-btn.active");
  if (activeTab) {
    const chartId = activeTab.getAttribute("onclick")?.match(/'(.+)'/)?.[1];
    if (chartId) showTab(null, chartId);
  }
});
