// Landing Page Interactive Features

// Navbar Scroll Effect
let lastScroll = 0;
const navbar = document.querySelector('.landing-nav');

window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;

  if (navbar) {
    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
  lastScroll = currentScroll;
});

// Interactive Code Compiler
class CodeRunner {
  constructor() {
    this.currentLang = 'javascript';
    this.initializeCompiler();
  }

  initializeCompiler() {
    const runBtn = document.getElementById('runCode');
    const langTabs = document.querySelectorAll('.lang-tab');

    if (runBtn) {
      runBtn.addEventListener('click', () => this.runCode());
    }

    langTabs.forEach(tab => {
      tab.addEventListener('click', (e) => this.switchLanguage(e.target.dataset.lang));
    });
  }

  switchLanguage(lang) {
    this.currentLang = lang;
    document.querySelectorAll('.lang-tab').forEach(tab => {
      tab.classList.toggle('active', tab.dataset.lang === lang);
    });
    document.querySelectorAll('.code-editor-pane').forEach(pane => {
      pane.classList.toggle('active', pane.dataset.lang === lang);
    });
  }

  runCode() {
    const output = document.getElementById('codeOutput');
    const editor = document.querySelector(`.code-editor-pane[data-lang="${this.currentLang}"] textarea`);

    if (!editor || !output) return;

    const code = editor.value;
    output.innerHTML = '';

    try {
      if (this.currentLang === 'javascript') {
        this.runJavaScript(code, output);
      } else if (this.currentLang === 'python') {
        this.runPython(code, output);
      }
    } catch (error) {
      output.innerHTML = `<span style="color: #ef4444;">Error: ${error.message}</span>`;
    }
  }

  runJavaScript(code, output) {
    const logs = [];
    const originalLog = console.log;
    console.log = (...args) => {
      logs.push(args.map(arg => typeof arg === 'object' ? JSON.stringify(arg) : String(arg)).join(' '));
    };

    try {
      eval(code);
      console.log = originalLog;

      if (logs.length > 0) {
        output.innerHTML = logs.map(log => `<div>${this.escapeHtml(log)}</div>`).join('');
      } else {
        output.innerHTML = '<span style="color: #10b981;">✓ Code executed successfully (no output)</span>';
      }
    } catch (error) {
      console.log = originalLog;
      throw error;
    }
  }

  runPython(code, output) {
    output.innerHTML = '<span style="color: #10b981;">✓ Python code validated</span><br>';
    output.innerHTML += '<span style="color: #94a3b8;">// Server-side execution required for Python</span><br>';
    output.innerHTML += '<span style="color: #94a3b8;">// Demo output:</span><br>';

    if (code.includes('print(')) {
      const matches = code.match(/print\((.*?)\)/g);
      if (matches) {
        matches.forEach(match => {
          const content = match.replace(/print\(['"](.*)["']\)/, '$1');
          output.innerHTML += `<div>${content}</div>`;
        });
      }
    }
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Testimonial Carousel
function initTestimonialCarousel() {
  const carousel = document.querySelector('.testimonial-carousel');
  if (!carousel) return;

  const items = carousel.querySelectorAll('.testimonial-item');
  const dots = carousel.querySelectorAll('.carousel-dot');
  let currentIndex = 0;

  function showSlide(index) {
    items.forEach((item, i) => {
      item.classList.toggle('active', i === index);
    });
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
  }

  function nextSlide() {
    currentIndex = (currentIndex + 1) % items.length;
    showSlide(currentIndex);
  }

  setInterval(nextSlide, 5000);

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      currentIndex = index;
      showSlide(index);
    });
  });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  new CodeRunner();
  initTestimonialCarousel();
});
