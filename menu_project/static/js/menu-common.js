// 공통 JavaScript 함수들

class MenuApp {
    constructor() {
        this.searchTimeout = null;
        this.init();
    }

    init() {
        // 브라우저가 멋대로 스크롤 위치를 복원하지 않도록 설정
        if ('scrollRestoration' in history) {
            history.scrollRestoration = 'manual';
        }

        this.initElements();
        this.bindEvents();
        this.initPageLoadActions();
    }

    initElements() {
        // 사이드 메뉴 요소들
        this.menuToggle = document.getElementById('menuToggle');
        this.sideMenu = document.getElementById('sideMenu');
        this.menuOverlay = document.getElementById('menuOverlay');
        this.closeMenu = document.getElementById('closeMenu');

        // 검색 요소들
        this.searchToggle = document.getElementById('searchToggle');
        this.searchContainer = document.getElementById('searchContainer');
        this.searchInput = document.getElementById('searchInput');
        this.searchClose = document.getElementById('searchClose');
        this.searchResults = document.getElementById('searchResults');
    }

    bindEvents() {
        // 사이드 메뉴 이벤트
        if (this.menuToggle) {
            this.menuToggle.addEventListener('click', () => this.openMenu());
            this.closeMenu.addEventListener('click', () => this.closeMenuFunc());
            this.menuOverlay.addEventListener('click', () => this.closeMenuFunc());
        }

        // 검색 이벤트
        if (this.searchToggle) {
            this.searchToggle.addEventListener('click', () => this.openSearch());
            this.searchClose.addEventListener('click', () => this.closeSearch());
            this.searchInput.addEventListener('input', () => this.performSearch());
        }

        // 스크롤 배경 효과
        this.initScrollBackground();
    }
    
    initPageLoadActions() {
        // 페이지 로드 시 스크롤
        document.addEventListener('DOMContentLoaded', () => this.scrollToTarget());
        window.addEventListener('load', () => {
            setTimeout(() => this.scrollToTarget(), 100); 
        });
    }

    // ==========================================
    // 스크롤 이동 기능
    // ==========================================
    scrollToTarget() {
        const urlParams = new URLSearchParams(window.location.search);
        const targetId = urlParams.get('target');

        if (!targetId) return;

        // 타겟 요소 찾기 (menu-숫자 또는 숫자 ID)
        let targetElement = document.getElementById('menu-' + targetId);
        if (!targetElement) targetElement = document.getElementById(targetId);

        if (targetElement) {
            // 화면 중앙으로 스크롤 이동
            targetElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'nearest'
            });
        }
    }

    // ==========================================
    // 검색 기능 (UI + Live Search)
    // ==========================================
    openSearch() {
        if (this.searchContainer) {
            this.searchContainer.style.display = 'flex';
        }
        if (this.searchInput) {
            this.searchInput.focus();
        }
    }

    closeSearch() {
        if (this.searchContainer) {
            this.searchContainer.style.display = 'none';
        }
        if (this.searchInput) {
            this.searchInput.value = '';
        }
        if (this.searchResults) {
            this.searchResults.innerHTML = '';
        }
    }

    performSearch() {
        const query = this.searchInput.value.trim();
        if (query.length < 2) {
            this.searchResults.innerHTML = '';
            return;
        }

        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => this.displaySearchResults(data.results))
                .catch(error => console.error(error));
        }, 300);
    }

    displaySearchResults(results) {
        if (results.length === 0) {
            this.searchResults.innerHTML = '<div class="search-no-results">검색 결과가 없습니다.</div>';
            return;
        }

        const html = results.map(result => `
            <div class="search-result-item" onclick="window.menuApp.handleSearchClick('${result.url}')">
                <div class="search-result-title">${result.title}</div>
                <div class="search-result-subtitle">${result.subtitle}</div>
            </div>
        `).join('');

        this.searchResults.innerHTML = html;
    }

    handleSearchClick(url) {
        let finalUrl = url;
        
        // URL에 #이 있으면 ?target= 파라미터로 변경하여 이동
        if (url.includes('#')) {
            const [baseUrl, anchor] = url.split('#');
            const cleanId = anchor.replace('menu-', ''); 
            
            const separator = baseUrl.includes('?') ? '&' : '?';
            finalUrl = `${baseUrl}${separator}target=${cleanId}`;
        }

        window.location.href = finalUrl;
    }

    // ==========================================
    // 사이드 메뉴 기능
    // ==========================================
    openMenu() {
        if (this.sideMenu) this.sideMenu.classList.add('active');
        if (this.menuOverlay) this.menuOverlay.classList.add('active');
    }

    closeMenuFunc() {
        if (this.sideMenu) this.sideMenu.classList.remove('active');
        if (this.menuOverlay) this.menuOverlay.classList.remove('active');
    }

    toggleCategory(categoryId) {
        const subCategories = document.getElementById('sub-' + categoryId);
        const icon = document.getElementById('icon-' + categoryId);
        if (subCategories.style.display === 'none') {
            subCategories.style.display = 'block';
            icon.textContent = '▼';
        } else {
            subCategories.style.display = 'none';
            icon.textContent = '▶';
        }
    }
    
    // 스크롤 배경 효과
    initScrollBackground() {
        const background = document.querySelector('.background-with-gradient');
        if (background) {
            window.addEventListener('scroll', function() {
                const scrollPercent = Math.min(window.scrollY / (document.documentElement.scrollHeight - window.innerHeight), 1);
                const scale = 1 + (scrollPercent * 1.8);
                background.style.transform = `scale(${scale})`;
            });
        }
    }
}

// 전역 함수로 노출 (템플릿에서 사용)
window.toggleCategory = function(categoryId) {
    if (window.menuApp) {
        window.menuApp.toggleCategory(categoryId);
    }
};

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
    window.menuApp = new MenuApp();
});
