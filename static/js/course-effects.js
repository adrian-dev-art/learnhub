// Module Tooltip Only (No Circle Ripple)
class ModuleTooltip {
  constructor() {
    this.tooltip = this.createTooltip();
    this.init();
  }

  createTooltip() {
    const tooltip = document.createElement('div');
    tooltip.id = 'moduleTooltip';
    tooltip.style.cssText = `
      position: fixed;
      z-index: 10000;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.3s ease;
      max-width: 300px;
    `;

    tooltip.innerHTML = `
      <div style="background: linear-gradient(135deg, rgba(30, 30, 45, 0.98), rgba(20, 20, 30, 0.98));
                  backdrop-filter: blur(20px);
                  padding: 20px;
                  border-radius: 16px;
                  border: 1px solid rgba(255, 107, 53, 0.3);
                  box-shadow: 0 20px 60px rgba(0,0,0,0.5);">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <span class="material-icons" style="color: #FF6B35; font-size: 20px;">list_alt</span>
          <span style="font-size: 14px; font-weight: 700; color: #fff;">Course Modules</span>
        </div>
        <ul id="tooltipModuleList" style="list-style: none; padding: 0; margin: 0; max-height: 300px; overflow-y: auto;">
        </ul>
      </div>
    `;

    document.body.appendChild(tooltip);
    return tooltip;
  }

  init() {
    this.courseModules = window.courseModulesData || {};

    // Use event delegation on document
    document.addEventListener('mouseenter', (e) => {
      // Check if target is an Element (not text node)
      if (e.target && e.target.nodeType === 1) {
        const card = e.target.closest('.course-card-modern');
        if (card) {
          const courseId = card.dataset.courseId;
          this.show(courseId);
        }
      }
    }, true);

    document.addEventListener('mousemove', (e) => {
      if (this.tooltip.style.opacity === '1') {
        this.position(e.clientX, e.clientY);
      }
    });

    document.addEventListener('mouseleave', (e) => {
      // Check if target is an Element
      if (e.target && e.target.nodeType === 1) {
        const card = e.target.closest('.course-card-modern');
        if (card) {
          this.hide();
        }
      }
    }, true);
  }

  show(courseId) {
    const modules = this.courseModules[courseId] || [];
    const list = document.getElementById('tooltipModuleList');
    if (!list) return;

    list.innerHTML = '';

    if (modules.length > 0) {
      modules.forEach(module => {
        const li = document.createElement('li');
        li.style.cssText = 'padding: 8px 0; display: flex; align-items: start; gap: 8px;';
        li.innerHTML = `
          <span class="material-icons" style="font-size: 16px; color: #FF6B35; margin-top: 2px;">check_circle</span>
          <span style="color: rgba(255,255,255,0.9); font-size: 13px; line-height: 1.4;">${module}</span>
        `;
        list.appendChild(li);
      });
    } else {
      list.innerHTML = '<li style="color: rgba(255,255,255,0.5); font-size: 13px; padding: 8px 0;">No modules yet</li>';
    }

    this.tooltip.style.opacity = '1';
  }

  hide() {
    this.tooltip.style.opacity = '0';
  }

  position(x, y) {
    const offsetX = 20;
    const offsetY = 20;
    let posX = x + offsetX;
    let posY = y + offsetY;

    const rect = this.tooltip.getBoundingClientRect();
    if (posX + rect.width > window.innerWidth) {
      posX = x - rect.width - offsetX;
    }
    if (posY + rect.height > window.innerHeight) {
      posY = y - rect.height - offsetY;
    }

    this.tooltip.style.left = posX + 'px';
    this.tooltip.style.top = posY + 'px';
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  new ModuleTooltip();
});
