/**
 * Demo version of Pomodoro Timer for testing color transitions
 * Uses 10-second timer instead of 25 minutes for quick testing
 */

class PomodoroTimerDemo {
    constructor() {
        // Timer state - shortened for demo
        this.totalTime = 10; // 10 seconds instead of 25 minutes
        this.currentTime = this.totalTime;
        this.isRunning = false;
        this.intervalId = null;
        
        // DOM elements
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.statusDisplay = document.querySelector('.status');
        this.progressContainer = document.querySelector('.progress');
        
        // Initialize components
        this.initializeElements();
        this.createCircularProgress();
        this.setupEventListeners();
        this.setupBackgroundEffects();
        
        // Update display
        this.updateDisplay();
        this.updateProgress();
    }
    
    initializeElements() {
        // Create circular progress container
        this.circularProgressContainer = document.createElement('div');
        this.circularProgressContainer.className = 'circular-progress-container';
        this.circularProgressContainer.innerHTML = `
            <svg class="circular-progress" width="200" height="200">
                <circle class="progress-bg" cx="100" cy="100" r="90"></circle>
                <circle class="progress-bar" cx="100" cy="100" r="90"></circle>
            </svg>
        `;
        
        // Replace linear progress with circular
        this.progressContainer.innerHTML = '';
        this.progressContainer.appendChild(this.circularProgressContainer);
    }
    
    createCircularProgress() {
        this.progressBar = document.querySelector('.progress-bar');
        this.progressBg = document.querySelector('.progress-bg');
        
        // Calculate circumference for progress calculation
        this.radius = 90;
        this.circumference = 2 * Math.PI * this.radius;
        
        // Set initial styles
        this.progressBar.style.strokeDasharray = this.circumference;
        this.progressBar.style.strokeDashoffset = 0;
    }
    
    setupEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleTimer());
        this.resetButton.addEventListener('click', () => this.resetTimer());
    }
    
    setupBackgroundEffects() {
        // Create particle container
        this.particleContainer = document.createElement('div');
        this.particleContainer.className = 'particle-container';
        document.body.appendChild(this.particleContainer);
        
        // Create ripple container
        this.rippleContainer = document.createElement('div');
        this.rippleContainer.className = 'ripple-container';
        document.body.appendChild(this.rippleContainer);
    }
    
    toggleTimer() {
        if (this.isRunning) {
            this.pauseTimer();
        } else {
            this.startTimer();
        }
    }
    
    startTimer() {
        this.isRunning = true;
        this.startButton.textContent = '一時停止';
        this.statusDisplay.textContent = '作業中';
        
        // Start background effects
        this.startBackgroundEffects();
        
        this.intervalId = setInterval(() => {
            if (this.currentTime > 0) {
                this.currentTime--;
                this.updateDisplay();
                this.updateProgress();
                this.updateColors();
            } else {
                this.completeTimer();
            }
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        this.statusDisplay.textContent = '一時停止中';
        
        // Stop background effects
        this.stopBackgroundEffects();
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    resetTimer() {
        this.pauseTimer();
        this.currentTime = this.totalTime;
        this.startButton.textContent = '開始';
        this.statusDisplay.textContent = '作業中';
        this.updateDisplay();
        this.updateProgress();
        this.updateColors();
        this.stopBackgroundEffects();
    }
    
    completeTimer() {
        this.pauseTimer();
        this.statusDisplay.textContent = '完了！';
        this.createCompletionEffect();
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.currentTime / 60);
        const seconds = this.currentTime % 60;
        this.timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    updateProgress() {
        const progress = (this.totalTime - this.currentTime) / this.totalTime;
        const offset = this.circumference * (1 - progress);
        this.progressBar.style.strokeDashoffset = offset;
        
        // Add smooth transition
        this.progressBar.style.transition = 'stroke-dashoffset 1s ease-in-out';
    }
    
    updateColors() {
        const progress = (this.totalTime - this.currentTime) / this.totalTime;
        
        // Color transition: blue (0%) -> yellow (50%) -> red (100%)
        let color;
        if (progress < 0.5) {
            // Blue to yellow
            const ratio = progress * 2;
            const r = Math.round(52 + (255 - 52) * ratio);
            const g = Math.round(152 + (255 - 152) * ratio);
            const b = Math.round(219 - 219 * ratio);
            color = `rgb(${r}, ${g}, ${b})`;
        } else {
            // Yellow to red
            const ratio = (progress - 0.5) * 2;
            const r = 255;
            const g = Math.round(255 - 24 * ratio);
            const b = Math.round(0 + 60 * ratio);
            color = `rgb(${r}, ${g}, ${b})`;
        }
        
        // Apply color to progress bar and time display
        this.progressBar.style.stroke = color;
        this.timeDisplay.style.color = color;
        
        // Update glow effect intensity
        const glowIntensity = progress * 20;
        this.progressBar.style.filter = `drop-shadow(0 0 ${glowIntensity}px ${color})`;
    }
    
    startBackgroundEffects() {
        // Start particle animation
        this.particleAnimation = setInterval(() => {
            this.createParticle();
        }, 500); // More frequent for demo
        
        // Start ripple animation
        this.rippleAnimation = setInterval(() => {
            this.createRipple();
        }, 2000);
    }
    
    stopBackgroundEffects() {
        if (this.particleAnimation) {
            clearInterval(this.particleAnimation);
            this.particleAnimation = null;
        }
        
        if (this.rippleAnimation) {
            clearInterval(this.rippleAnimation);
            this.rippleAnimation = null;
        }
        
        // Clear existing particles and ripples
        this.particleContainer.innerHTML = '';
        this.rippleContainer.innerHTML = '';
    }
    
    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random position and properties
        const x = Math.random() * window.innerWidth;
        const y = window.innerHeight + 10;
        const size = Math.random() * 4 + 2;
        const duration = Math.random() * 3000 + 2000;
        
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        
        this.particleContainer.appendChild(particle);
        
        // Animate particle
        particle.animate([
            { transform: 'translateY(0) rotate(0deg)', opacity: 0 },
            { transform: 'translateY(-50px) rotate(180deg)', opacity: 1, offset: 0.1 },
            { transform: `translateY(-${window.innerHeight + 100}px) rotate(360deg)`, opacity: 0 }
        ], {
            duration: duration,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        }).onfinish = () => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        };
    }
    
    createRipple() {
        const ripple = document.createElement('div');
        ripple.className = 'ripple';
        
        // Center the ripple
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        
        ripple.style.left = centerX + 'px';
        ripple.style.top = centerY + 'px';
        
        this.rippleContainer.appendChild(ripple);
        
        // Animate ripple
        ripple.animate([
            { transform: 'translate(-50%, -50%) scale(0)', opacity: 0.8 },
            { transform: 'translate(-50%, -50%) scale(1)', opacity: 0.4, offset: 0.5 },
            { transform: 'translate(-50%, -50%) scale(2)', opacity: 0 }
        ], {
            duration: 3000,
            easing: 'ease-out'
        }).onfinish = () => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        };
    }
    
    createCompletionEffect() {
        // Create celebration particles
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const particle = document.createElement('div');
                particle.className = 'celebration-particle';
                
                const x = window.innerWidth / 2 + (Math.random() - 0.5) * 200;
                const y = window.innerHeight / 2 + (Math.random() - 0.5) * 200;
                
                particle.style.left = x + 'px';
                particle.style.top = y + 'px';
                
                document.body.appendChild(particle);
                
                particle.animate([
                    { transform: 'scale(0) rotate(0deg)', opacity: 1 },
                    { transform: 'scale(1) rotate(180deg)', opacity: 1, offset: 0.5 },
                    { transform: 'scale(0) rotate(360deg)', opacity: 0 }
                ], {
                    duration: 1500,
                    easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
                }).onfinish = () => {
                    if (particle.parentNode) {
                        particle.parentNode.removeChild(particle);
                    }
                };
            }, i * 100);
        }
    }
}

// Use demo timer for testing
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimerDemo();
});