// Ultra Smooth Scroll for Mouse/Trackpad
class SmoothScroll {
  constructor() {
    this.currentScroll = window.pageYOffset;
    this.targetScroll = window.pageYOffset;
    this.ease = 0.08;
    this.isScrolling = false;
    this.rafId = null;
    this.init();
  }

  init() {
    // Prevent default scroll behavior
    window.addEventListener('wheel', (e) => {
      e.preventDefault();

      // Add scroll delta to target
      this.targetScroll += e.deltaY;

      // Clamp target scroll
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      this.targetScroll = Math.max(0, Math.min(this.targetScroll, maxScroll));

      // Start smooth scrolling if not already running
      if (!this.isScrolling) {
        this.isScrolling = true;
        this.smoothScroll();
      }
    }, { passive: false });

    // Handle keyboard scrolling (no space key, allow Ctrl/Alt/Shift combinations)
    const keys = [33, 34, 35, 36, 38, 40];
    window.addEventListener('keydown', (e) => {
      // Don't block if any modifier key is pressed (allows Ctrl+Tab, Alt+Tab, etc)
      if (e.ctrlKey || e.altKey || e.metaKey || e.shiftKey) {
        return;
      }

      if (keys.includes(e.keyCode)) {
        e.preventDefault();

        let delta = 0;
        switch (e.keyCode) {
          case 38: delta = -100; break; // Up arrow
          case 40: delta = 100; break;  // Down arrow
          case 33: delta = -window.innerHeight; break; // Page up
          case 34: delta = window.innerHeight; break;  // Page down
          case 36: this.targetScroll = 0; break; // Home
          case 35: this.targetScroll = document.documentElement.scrollHeight; break; // End
        }

        this.targetScroll += delta;
        const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
        this.targetScroll = Math.max(0, Math.min(this.targetScroll, maxScroll));

        if (!this.isScrolling) {
          this.isScrolling = true;
          this.smoothScroll();
        }
      }
    });
  }

  smoothScroll() {
    const diff = this.targetScroll - this.currentScroll;

    // Continue animating if difference is significant
    if (Math.abs(diff) > 0.5) {
      this.currentScroll += diff * this.ease;
      window.scrollTo(0, this.currentScroll);
      this.rafId = requestAnimationFrame(() => this.smoothScroll());
    } else {
      // Snap to target when close enough
      this.currentScroll = this.targetScroll;
      window.scrollTo(0, this.currentScroll);
      this.isScrolling = false;
      if (this.rafId) {
        cancelAnimationFrame(this.rafId);
        this.rafId = null;
      }
    }
  }

  // Method to programmatically scroll to a position
  scrollTo(target) {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    this.targetScroll = Math.max(0, Math.min(target, maxScroll));

    if (!this.isScrolling) {
      this.isScrolling = true;
      this.smoothScroll();
    }
  }
}

// Initialize and export
const smoothScrollInstance = new SmoothScroll();

// Make it available globally for programmatic scrolling
window.smoothScrollTo = (target) => smoothScrollInstance.scrollTo(target);
