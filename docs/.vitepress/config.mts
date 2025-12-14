import { defineConfig } from 'vitepress'

export default defineConfig({
    lang: 'en-US',
    title: 'goatmilkkk',
    description: 'personal website for my blog posts & CTF writeups',
    head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
    titleTemplate: false,
    themeConfig: {
        sidebar: {
            "/writeups/": [
                {
                    "text": "2025",
                    "items": [
                        {
                            "text": "SECCON",
                            "collapsed": true,
                            "items": [
                                {
                                    "text": "ez-flag-checker (Rev)",
                                    "link": "/writeups/2025/SECCON/ez-flag-checker/writeup"
                                }
                            ]
                        },
                        {
                            "text": "CyKor",
                            "collapsed": true,
                            "items": [
                                {
                                    "text": "ex-cute (Rev)",
                                    "link": "/writeups/2025/CyKor/ex-cute/writeup"
                                }
                            ]
                        },
                        {
                            "text": "ASEAN Cyber Shield",
                            "collapsed": true,
                            "items": [
                                {
                                    "text": "Gateway Interface (Pwn, Iot)",
                                    "link": "/writeups/2025/ASEAN%20Cyber%20Shield/Gateway%20Interface/writeup"
                                },
                                {
                                    "text": "pumpguardian (Rev)",
                                    "link": "/writeups/2025/ASEAN%20Cyber%20Shield/pumpguardian/writeup"
                                }
                            ]
                        },
                        {
                            "text": "Cyber SEA Games",
                            "collapsed": true,
                            "items": [
                                {
                                    "text": "RE & Network (Forensics)",
                                    "link": "/writeups/2025/Cyber%20SEA%20Games/India%20-%20Reversing%20%26%20Network/writeup"
                                },
                                {
                                    "text": "Matryoshka (Rev)",
                                    "link": "/writeups/2025/Cyber%20SEA%20Games/Russia%20-%20Matryoshka/writeup"
                                }
                            ]
                        }
                    ]
                }
            ],
            "/notes/": [
                {
                    "text": "Notes",
                    "items": [
                        {
                            "text": "Docker",
                            "link": "/notes/docker"
                        },
                        {
                            "text": "Linux",
                            "link": "/notes/linux"
                        },
                        {
                            "text": "Mobile",
                            "link": "/notes/mobile"
                        },
                        {
                            "text": "Rust",
                            "link": "/notes/rust"
                        },
                        {
                            "text": "SEH",
                            "link": "/notes/seh"
                        }
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
