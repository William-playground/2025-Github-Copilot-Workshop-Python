// 設定モーダル管理

class SettingsManager {
    constructor() {
        this.modal = document.getElementById('settings-modal');
        this.settingsBtn = document.getElementById('settings-btn');
        this.closeBtn = document.querySelector('.close');
        this.saveBtn = document.getElementById('save-settings');
        this.cancelBtn = document.getElementById('cancel-settings');
        
        this.workDurationSelect = document.getElementById('work-duration');
        this.breakDurationSelect = document.getElementById('break-duration');
        this.themeSelect = document.getElementById('theme');
        this.soundStartCheckbox = document.getElementById('sound-start');
        this.soundEndCheckbox = document.getElementById('sound-end');
        this.soundTickCheckbox = document.getElementById('sound-tick');
        
        this.bindEvents();
    }

    bindEvents() {
        this.settingsBtn.addEventListener('click', () => this.openModal());
        this.closeBtn.addEventListener('click', () => this.closeModal());
        this.cancelBtn.addEventListener('click', () => this.closeModal());
        this.saveBtn.addEventListener('click', () => this.saveSettings());
        
        // モーダル外クリックで閉じる
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
        
        // ESCキーで閉じる
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modal.style.display === 'block') {
                this.closeModal();
            }
        });
    }

    openModal() {
        this.loadCurrentSettings();
        this.modal.style.display = 'block';
    }

    closeModal() {
        this.modal.style.display = 'none';
    }

    loadCurrentSettings() {
        const timer = window.pomodoroTimer;
        if (!timer) return;
        
        this.workDurationSelect.value = timer.settings.workDuration;
        this.breakDurationSelect.value = timer.settings.breakDuration;
        this.themeSelect.value = timer.settings.theme;
        this.soundStartCheckbox.checked = timer.settings.sounds.start;
        this.soundEndCheckbox.checked = timer.settings.sounds.end;
        this.soundTickCheckbox.checked = timer.settings.sounds.tick;
    }

    saveSettings() {
        const newSettings = {
            workDuration: parseInt(this.workDurationSelect.value),
            breakDuration: parseInt(this.breakDurationSelect.value),
            theme: this.themeSelect.value,
            sounds: {
                start: this.soundStartCheckbox.checked,
                end: this.soundEndCheckbox.checked,
                tick: this.soundTickCheckbox.checked
            }
        };
        
        const timer = window.pomodoroTimer;
        if (timer) {
            timer.updateSettings(newSettings);
        }
        
        this.closeModal();
    }
}

// タイマーが初期化された後に設定マネージャーを初期化
document.addEventListener('DOMContentLoaded', () => {
    // タイマーの初期化を少し待つ
    setTimeout(() => {
        window.settingsManager = new SettingsManager();
    }, 100);
});