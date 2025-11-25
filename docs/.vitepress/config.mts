import { defineConfig } from 'vitepress'

export default defineConfig({
    lang: 'en-US',
    title: 'goatmilkkk',
    description: 'personal website for my blog posts & CTF writeups',
    titleTemplate: false,
    themeConfig: {
        sidebar: [
            {
                text: '2025',
                items: [
                    { 
                        text: 'ASEAN Cyber Shield', 
                        collapsed: true,
                        items: []
                    },
                    { 
                        text: 'ICC Tokyo', 
                        collapsed: true,
                        items: []
                    },
                    { 
                        // Add newline in text using <br>
                        text: 'Cyber SEA Games', 
                        collapsed: true,
                        items: [
                            { text: 'RE & Network', link: '/writeups/2025/Cyber%20SEA%20Games/India%20-%20Reversing%20%26%20Network/writeup' },
                            { text: 'Matryoshka', link: '/writeups/2025/Cyber%20SEA%20Games/Russia%20-%20Matryoshka/writeup' },
                        ]   
                    }
                ]
            },
        ],
        
        search: { provider: 'local' },
        siteTitle: 'Home',
        logo: '/favico.ico',

        socialLinks: [
            { icon: 'github', link: 'https://github.com/goatmilkkk' },
            { icon: 'twitter', link: 'https://x.com/goatmilkkk' }
        ]
    }
})
