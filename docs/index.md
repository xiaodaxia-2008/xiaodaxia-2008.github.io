---
description: Shawn的个人博客
hide:
  - navigation
  - toc
  - footer
---

# [Shawn](blog/index.md) { .center }

![](./images/sleepy-cat.png){ width="300px" data-title="路边两只互相依偎熟睡的橘猫" }
///caption
///

[:fontawesome-solid-blog:](blog/index.md)
&nbsp;
[:simple-bilibili:](https://space.bilibili.com/231692492/dynamic?spm_id_from=333.1365.my-info.dyns.click)
&nbsp;
[:simple-github:](https://github.com/xiaodaxia-2008)
&nbsp;
[:simple-csdn:](https://blog.csdn.net/xiaozisheng2008_)
&nbsp;
[:simple-rss:](/feed_rss_created.xml)
&nbsp;
[🎇](./interesting/fireworks.html)
{ .center }

<div style="text-align: center;">
    <p id="typewriter-title" class="title-typewriter"></p>
    
    <p id="typewriter-quote" class="quote-typewriter" style="visibility: hidden;"></p>
    
    <div id="redirect-controls" style="visibility: hidden; margin-top: 1.5em;">
        <div style="display: flex; justify-content: center; align-items: center; flex-wrap: wrap;">
            <p id="redirect-message" class="redirect-text"></p>
            <div style="margin: 5px;">
                <button id="redirect-now-btn" class="redirect-btn">迫不及待</button>
                <button id="cancel-redirect-btn" class="redirect-btn">留在这里</button>
            </div>
        </div>
    </div>
</div>

<style>
    /* 标题样式 */
    .title-typewriter {
        font-size: 1.1em;
        font-weight: bold;
        font-family: 'KaiTi', 'STKaiti', '楷体', serif;
        margin-bottom: 1.5em; /* 增加与下方引文的间距 */
    }
    /* 引文样式 */
    .quote-typewriter {
        font-size: 1.1em;
        font-family: 'KaiTi', 'STKaiti', '楷体', serif;
    }
    /* 跳转提示文字样式 */
    .redirect-text {
        color: #aaaaaa; 
        font-size: 0.9em; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
        margin: 5px;
    }
    /* 闪烁的光标效果 (通用) */
    .typing-cursor::after {
        content: '▋';
        display: inline-block;
        animation: blink-caret .75s step-end infinite;
        color: #ff6347;
        margin-left: 0.2em;
    }
    @keyframes blink-caret {
        from, to { opacity: 1; }
        50% { opacity: 0; }
    }
    /* 跳转按钮样式 */
    .redirect-btn {
        background: none; border: none; padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #999;
        font-size: 0.9em;
        margin: 0 8px;
        cursor: pointer;
        transition: color 0.2s;
    }
    .redirect-btn:hover {
        color: #333;
        text-decoration: underline;
    }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // -- 要显示的文本 --
    // 注意：我们直接使用 Emoji 字符 🐎 和 ⚔️，比 Markdown 短代码更可靠
    const titleText = "🐎 出门搔白首，若负平生志 ⚔️";
    const quoteText = "我所渴求的，无非是将心中脱颖欲出的本性付诸生活。为什么竟如此艰难呢？";

    // -- 获取元素 --
    const titleElement = document.getElementById('typewriter-title');
    const quoteElement = document.getElementById('typewriter-quote');
    const redirectControlsElement = document.getElementById('redirect-controls');
    const redirectMessageElement = document.getElementById('redirect-message');
    const redirectNowBtn = document.getElementById('redirect-now-btn');
    const cancelRedirectBtn = document.getElementById('cancel-redirect-btn');

    let countdownInterval;

    // -- 核心功能函数 --
    function typeWriter(element, text, speed, onComplete) {
        let i = 0;
        element.classList.add('typing-cursor');
        const interval = setInterval(() => {
            if (i < text.length) {
                element.innerHTML = text.substring(0, i + 1);
                i++;
            } else {
                clearInterval(interval);
                element.classList.remove('typing-cursor');
                if (onComplete) onComplete();
            }
        }, speed);
    }

    function startRedirectCountdown(seconds) {
        redirectControlsElement.style.visibility = 'visible';
        let remaining = seconds;
        const updateMessage = () => {
            redirectMessageElement.innerHTML = `<strong>${remaining}</strong> 秒后自动前往博客...`;
        };
        updateMessage();
        countdownInterval = setInterval(() => {
            remaining--;
            updateMessage();
            if (remaining <= 0) {
                clearInterval(countdownInterval);
                window.location.href = '/blog';
            }
        }, 1000);
    }

    // -- 按钮事件 --
    redirectNowBtn.addEventListener('click', () => {
        if(countdownInterval) clearInterval(countdownInterval);
        window.location.href = '/blog';
    });
    
    cancelRedirectBtn.addEventListener('click', () => {
        if(countdownInterval) clearInterval(countdownInterval);
        redirectControlsElement.style.visibility = 'hidden';
    });

    // -- **动画执行链** --
    // 1. 首先，执行标题的打字机动画
    typeWriter(titleElement, titleText, 150, () => {
        // 2. 标题完成后，让引文容器可见，并开始引文的打字机动画
        quoteElement.style.visibility = 'visible';
        typeWriter(quoteElement, quoteText, 120, () => {
            // 3. 引文完成后，等待片刻，然后启动跳转倒计时
            setTimeout(() => {
                startRedirectCountdown(5);
            }, 500);
        });
    });
});
</script>


<!-- hide view/edit source for home page https://github.com/squidfunk/mkdocs-material/discussions/5064 -->
<style>
  .md-content__button {
    display: none;
  }
</style>