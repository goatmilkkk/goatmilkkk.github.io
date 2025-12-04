import { defineConfig } from 'vitepress'

export default defineConfig({
    lang: 'en-US',
    title: 'goatmilkkk',
    description: 'personal website for my blog posts & CTF writeups',
    head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
    titleTemplate: false,
    themeConfig: {
        sidebar: {
            '/writeups/': [
                {
                    text: '2025',
                    items: [
                        // overseas
                        { 
                            text: 'ASEAN Cyber Shield', 
                            collapsed: true,
                            items: [
                                { text: 'pumpguardian (Rev)', link: '/writeups/2025/ASEAN%20Cyber%20Shield/pumpguardian/writeup'},
                                { text: 'Gateway Interface (Pwn)', link: '/writeups/2025/ASEAN%20Cyber%20Shield/Gateway%20Interface/writeup'},
                                { text: 'Scenario Step5 (Rev, Pwn)', link: '/'},
                            ]
                        },
                        { 
                            text: 'Cyber SEA Games', 
                            collapsed: true,
                            items: [
                                { text: 'RE & Network (Forensics)', link: '/writeups/2025/Cyber%20SEA%20Games/India%20-%20Reversing%20%26%20Network/writeup' },
                                { text: 'Matryoshka (Rev)', link: '/writeups/2025/Cyber%20SEA%20Games/Russia%20-%20Matryoshka/writeup' },
                            ]   
                        },

                        // online
                        { 
                            text: 'Infobahn', 
                            collapsed: true,
                            items: []
                        }
                    ]
                }
            ],

            '/notes/': [
                 {
                    text: 'Notes',
                    items: [
                        { text: 'Remote Debugging', link: '/notes/remote-dbg'},
                        { text: 'Docker', link: '/notes/docker'},
                        { text: 'Rust', link: '/notes/rust'},
                        { text: 'Mobile', link: '/notes/mobile'},
                    ]
                }
            ]

        },
        
        search: { provider: 'local' },
        siteTitle: 'Home',

        nav: [
            { text: 'Writeups', link: '/writeups/2025/ASEAN%20Cyber%20Shield/pumpguardian/writeup' },
            { text: 'Notes', link: '/notes/remote-dbg' },
        ],

        socialLinks: [
            { icon: 'github', link: 'https://github.com/goatmilkkk' },
            { icon: 'twitter', link: 'https://x.com/goatmilkkk' }
        ]
    }
})
