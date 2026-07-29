(() => {
  const initializeTabOverflow = () => {
    const tabs = document.querySelector("[data-md-component='tabs']");
    const list = tabs?.querySelector(".md-tabs__list");
    const inner = list?.parentElement;

    if (!tabs || !inner || !list || inner.classList.contains("rag-tabs-enhanced")) {
      return;
    }

    const createButton = (direction, label, glyph) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `rag-tabs-scroll rag-tabs-scroll--${direction}`;
      button.setAttribute("aria-label", label);
      button.textContent = glyph;
      return button;
    };

    const leftButton = createButton("left", "Scroll navigation left", "\u2039");
    const rightButton = createButton("right", "Scroll navigation right", "\u203a");

    inner.classList.add("rag-tabs-enhanced");
    inner.prepend(leftButton);
    inner.append(rightButton);

    const updateControls = () => {
      const maximum = Math.max(0, list.scrollWidth - list.clientWidth);
      const overflowing = maximum > 1;

      inner.classList.toggle("rag-tabs-overflowing", overflowing);
      leftButton.disabled = !overflowing || list.scrollLeft <= 1;
      rightButton.disabled = !overflowing || list.scrollLeft >= maximum - 1;
    };

    const scrollTabs = (direction) => {
      const distance = Math.max(320, list.clientWidth * 0.65);
      list.scrollBy({ left: direction * distance, behavior: "smooth" });
    };

    leftButton.addEventListener("click", () => scrollTabs(-1));
    rightButton.addEventListener("click", () => scrollTabs(1));
    list.addEventListener("scroll", updateControls, { passive: true });

    const resizeObserver = new ResizeObserver(updateControls);
    resizeObserver.observe(inner);
    resizeObserver.observe(list);

    requestAnimationFrame(() => {
      const activeTab = list.querySelector(".md-tabs__item--active");

      if (activeTab) {
        const maximum = Math.max(0, list.scrollWidth - list.clientWidth);
        const centered = activeTab.offsetLeft
          - ((list.clientWidth - activeTab.offsetWidth) / 2);

        list.style.scrollBehavior = "auto";
        list.scrollLeft = Math.min(maximum, Math.max(0, centered));

        requestAnimationFrame(() => {
          list.style.removeProperty("scroll-behavior");
          updateControls();
        });
      }

      updateControls();
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeTabOverflow, { once: true });
  } else {
    initializeTabOverflow();
  }
})();
