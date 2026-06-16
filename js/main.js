// --- AUREUM METAIS E-COMMERCE CORE LOGIC ---

document.addEventListener('DOMContentLoaded', () => {
  // Global Cart State
  let cart = JSON.parse(localStorage.getItem('aureum_cart')) || [];

  // DOM Elements - General
  const header = document.querySelector('header');
  const cartDrawer = document.getElementById('cart-drawer');
  const cartBackdrop = document.getElementById('cart-backdrop');
  const cartToggleBtn = document.getElementById('cart-toggle-btn');
  const cartCloseBtn = document.getElementById('cart-close-btn');
  const cartItemCountNav = document.getElementById('cart-count-nav');
  const cartDrawerContent = document.getElementById('cart-drawer-content');
  const cartTotalVal = document.getElementById('cart-total-val');
  const toastContainer = document.getElementById('toast-container');
  
  // Mobile Nav DOM Elements
  const menuToggle = document.getElementById('menu-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  const mobileNavClose = document.getElementById('mobile-nav-close');

  // Initialize UI components
  initScrollHeader();
  initCartEvents();
  renderCart();
  initMobileNav();
  
  // Initialize Product Page Specific Elements
  if (document.body.classList.contains('product-page')) {
    initProductPage();
  }

  // --- HEADER SCROLL ACTION ---
  function initScrollHeader() {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // --- CART DRAWER & EVENTS ---
  function initCartEvents() {
    if (cartToggleBtn) {
      cartToggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        toggleCart(true);
      });
    }
    
    if (cartCloseBtn) {
      cartCloseBtn.addEventListener('click', () => toggleCart(false));
    }
    
    if (cartBackdrop) {
      cartBackdrop.addEventListener('click', () => toggleCart(false));
    }
  }

  function toggleCart(open) {
    if (open) {
      cartDrawer.classList.add('active');
      cartBackdrop.classList.add('active');
      document.body.style.overflow = 'hidden'; // Lock background scroll
    } else {
      cartDrawer.classList.remove('active');
      cartBackdrop.classList.remove('active');
      document.body.style.overflow = ''; // Unlock scroll
    }
  }

  // Save cart state
  function saveCart() {
    localStorage.setItem('aureum_cart', JSON.stringify(cart));
    renderCart();
  }

  // Render cart content
  function renderCart() {
    // Nav count update
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (cartItemCountNav) {
      cartItemCountNav.textContent = totalItems;
      cartItemCountNav.style.display = totalItems > 0 ? 'flex' : 'none';
    }

    if (!cartDrawerContent) return;

    if (cart.length === 0) {
      cartDrawerContent.innerHTML = `
        <div class="cart-empty-message">
          <p>Sua sacola está vazia.</p>
          <a href="index.html#produtos" class="btn btn-primary" style="margin-top: 1.5rem; display: inline-block; padding: 0.75rem 1.5rem; font-size: 0.75rem;" onclick="document.getElementById('cart-close-btn').click();">Explorar Metais</a>
        </div>
      `;
      cartTotalVal.textContent = 'R$ 0,00';
      return;
    }

    let cartHtml = '';
    let totalPrice = 0;

    cart.forEach((item, index) => {
      const itemPriceTotal = item.price * item.quantity;
      totalPrice += itemPriceTotal;
      
      cartHtml += `
        <div class="cart-item">
          <img src="${item.image}" alt="${item.name}" class="cart-item-img">
          <div class="cart-item-details">
            <div>
              <div class="cart-item-name">${item.name}</div>
              <div class="cart-item-variant">${item.variant}</div>
            </div>
            <div class="cart-item-bottom">
              <div class="cart-item-qty">
                <button class="cart-item-qty-btn minus" data-index="${index}">-</button>
                <div class="cart-item-qty-val">${item.quantity}</div>
                <button class="cart-item-qty-btn plus" data-index="${index}">+</button>
              </div>
              <div class="cart-item-price">R$ ${itemPriceTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</div>
            </div>
            <button class="cart-item-remove" data-index="${index}">Remover</button>
          </div>
        </div>
      `;
    });

    cartDrawerContent.innerHTML = cartHtml;
    cartTotalVal.textContent = `R$ ${totalPrice.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    // Hook listeners for cart actions
    const removeBtns = cartDrawerContent.querySelectorAll('.cart-item-remove');
    removeBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.target.dataset.index);
        removeItem(index);
      });
    });

    const minusBtns = cartDrawerContent.querySelectorAll('.cart-item-qty-btn.minus');
    minusBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.currentTarget.dataset.index);
        updateItemQuantity(index, -1);
      });
    });

    const plusBtns = cartDrawerContent.querySelectorAll('.cart-item-qty-btn.plus');
    plusBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.currentTarget.dataset.index);
        updateItemQuantity(index, 1);
      });
    });
  }

  function removeItem(index) {
    const item = cart[index];
    cart.splice(index, 1);
    saveCart();
    showToast(`${item.name} removido da sacola.`);
  }

  function updateItemQuantity(index, delta) {
    cart[index].quantity += delta;
    if (cart[index].quantity <= 0) {
      removeItem(index);
    } else {
      saveCart();
    }
  }

  // Expose global function to add items
  window.addToCartGlobal = function(id, name, price, image, variant) {
    const existingIndex = cart.findIndex(item => item.id === id && item.variant === variant);
    
    if (existingIndex > -1) {
      cart[existingIndex].quantity += 1;
    } else {
      cart.push({
        id,
        name,
        price,
        image,
        variant,
        quantity: 1
      });
    }
    
    saveCart();
    showToast(`${name} (${variant}) adicionado à sacola.`);
    toggleCart(true); // Open the drawer
  };

  // --- TOAST NOTIFICATIONS ---
  function showToast(message) {
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--color-accent); flex-shrink:0;"><polyline points="20 6 9 17 4 12"></polyline></svg>
      <span>${message}</span>
    `;
    toastContainer.appendChild(toast);
    
    // Force reflow and add animation class
    setTimeout(() => toast.classList.add('show'), 50);
    
    // Auto remove
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 400);
    }, 3500);
  }

  // --- MOBILE NAVIGATION DRAWER ---
  function initMobileNav() {
    if (menuToggle && mobileNav) {
      menuToggle.addEventListener('click', (e) => {
        e.preventDefault();
        mobileNav.classList.add('active');
        cartBackdrop.classList.add('active'); // Reuse cart backdrop for overlay
      });
    }

    if (mobileNavClose) {
      mobileNavClose.addEventListener('click', () => {
        mobileNav.classList.remove('active');
        cartBackdrop.classList.remove('active');
      });
    }

    // Adapt backdrop listener to close mobile navigation as well
    if (cartBackdrop) {
      cartBackdrop.addEventListener('click', () => {
        if (mobileNav) mobileNav.classList.remove('active');
      });
    }
  }

  // --- PRODUCT PAGE DETAIL LOGIC ---
  function initProductPage() {
    const mainImgViewport = document.getElementById('main-image-viewport');
    const mainImg = mainImgViewport ? mainImgViewport.querySelector('img') : null;
    const thumbs = document.querySelectorAll('.gallery-thumb');
    const finishBtns = document.querySelectorAll('.finish-btn');
    const configVariantText = document.getElementById('config-variant-text');
    const btnAddToCart = document.getElementById('add-to-cart-btn');
    const qtyInput = document.getElementById('qty-input');
    const qtyMinus = document.getElementById('qty-minus');
    const qtyPlus = document.getElementById('qty-plus');
    const specHeaders = document.querySelectorAll('.spec-header');

    // 1. Thumbnail selection
    thumbs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        thumbs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        if (mainImg) {
          mainImg.src = thumb.querySelector('img').src;
        }
      });
    });

    // 2. Zoom magnifier on hover
    if (mainImgViewport && mainImg) {
      mainImgViewport.addEventListener('mousemove', (e) => {
        const rect = mainImgViewport.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width) * 100;
        const y = ((e.clientY - rect.top) / rect.height) * 100;
        
        mainImg.style.transformOrigin = `${x}% ${y}%`;
        mainImg.style.transform = 'scale(1.8)';
      });
      
      mainImgViewport.addEventListener('mouseleave', () => {
        mainImg.style.transform = 'scale(1)';
        mainImg.style.transformOrigin = 'center center';
      });
    }

    // 3. Variant selector
    let selectedVariantName = 'Dourado Escovado'; // Default selected variant
    finishBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        finishBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        const variant = btn.dataset.variant;
        selectedVariantName = btn.dataset.variantName;
        
        if (configVariantText) {
          configVariantText.textContent = selectedVariantName;
        }
        
        // Update product images if studio colors are bound
        if (variant === 'black' && mainImg) {
          mainImg.src = 'img/prod_torneira_parede.png';
        } else if (variant === 'gold' && mainImg) {
          mainImg.src = 'img/prod_misturador_dourado.png';
        } else if (variant === 'chrome' && mainImg) {
          mainImg.src = 'img/prod_gourmet_black.png'; // Fallback / mockup update
        }
        
        // Find corresponding thumbnail if applicable
        thumbs.forEach((t, i) => {
          if (i === 0 && variant === 'gold') t.click();
          if (i === 1 && variant === 'black') t.click();
        });
      });
    });

    // 4. Quantity Controls
    if (qtyMinus && qtyPlus && qtyInput) {
      qtyMinus.addEventListener('click', () => {
        let val = parseInt(qtyInput.value) || 1;
        if (val > 1) {
          qtyInput.value = val - 1;
        }
      });
      
      qtyPlus.addEventListener('click', () => {
        let val = parseInt(qtyInput.value) || 1;
        qtyInput.value = val + 1;
      });

      qtyInput.addEventListener('change', () => {
        let val = parseInt(qtyInput.value) || 1;
        if (val < 1) qtyInput.value = 1;
      });
    }

    // 5. Accordion Tabs
    specHeaders.forEach(header => {
      header.addEventListener('click', () => {
        const item = header.closest('.spec-item');
        const isActive = item.classList.contains('active');
        
        // Close other items
        document.querySelectorAll('.spec-item').forEach(i => i.classList.remove('active'));
        
        if (!isActive) {
          item.classList.add('active');
        }
      });
    });

    // 6. Add to Cart integration
    if (btnAddToCart) {
      btnAddToCart.addEventListener('click', () => {
        const prodId = btnAddToCart.dataset.productId || 'star-product';
        const prodName = btnAddToCart.dataset.productName || 'Misturador Monocomando Aureum';
        const prodPrice = parseFloat(btnAddToCart.dataset.productPrice) || 1890.00;
        const prodImage = mainImg ? mainImg.src : 'img/prod_misturador_dourado.png';
        const quantity = parseInt(qtyInput ? qtyInput.value : 1) || 1;

        // Loop to add multiple quantity if desired, or alter window.addToCartGlobal to support qty.
        // Let's modify adding to cart logic for custom quantities:
        const existingIndex = cart.findIndex(item => item.id === prodId && item.variant === selectedVariantName);
        
        if (existingIndex > -1) {
          cart[existingIndex].quantity += quantity;
        } else {
          cart.push({
            id: prodId,
            name: prodName,
            price: prodPrice,
            image: prodImage,
            variant: selectedVariantName,
            quantity: quantity
          });
        }
        
        saveCart();
        showToast(`${prodName} (${selectedVariantName}) adicionado à sacola.`);
        toggleCart(true);
      });
    }
  }
});
