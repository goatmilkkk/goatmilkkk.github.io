import { defineConfig } from 'vitepress'

export default defineConfig({
    lang: 'en-US',
    title: 'goatmilkkk',
    description: 'personal website for my blog posts & CTF writeups',
    head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
    titleTemplate: false,
    themeConfig: {
        sidebar: [
            {
                text: '2025',
                items: [
                    // overseas
                    { 
                        text: 'ASEAN Cyber Shield', 
                        collapsed: true,
                        items: [
                            { text: 'Pump Guardian (Rev)', link: '/'},
                            { text: 'Gateway Interface (Pwn)', link: '/'},
                            { text: 'VoIP Stealer (Forensics)', link: '/'},
                            { text: 'Scenario Step5 (Rev, Pwn)', link: '/'},
                            { text: 'Silent AIS (Rev, Crypto)', link: '/'},
                        ]
                    },
                    { 
                        text: 'ICC Tokyo', 
                        collapsed: true,
                        items: []
                    },
                    { 
                        // add newline in text using <br>
                        text: 'Cyber SEA Games', 
                        collapsed: true,
                        items: [
                            { text: 'RE & Network (Forensics)', link: '/writeups/2025/Cyber%20SEA%20Games/India%20-%20Reversing%20%26%20Network/writeup' },
                            { text: 'Matryoshka (Rev)', link: '/writeups/2025/Cyber%20SEA%20Games/Russia%20-%20Matryoshka/writeup' },
                        ]   
                    },
                    {
                        text: 'ASEAN Open', 
                        collapsed: true,
                        items: []
                    },

                    // online
                    {
                        text: 'N1CTF', 
                        collapsed: true,
                        items: []   
                    },
                    { 
                        text: 'Infobahn', 
                        collapsed: true,
                        items: []
                    },

                    // local
                    { 
                        text: 'TISC', 
                        collapsed: true,
                        items: [
                            { text: 'Challenge 7 (Cloud)', link: '/'},
                            { text: 'Challenge 8 (Web)', link: '/'},
                            { text: 'Challenge 9 (Hardware, Pwn)', link: '/'},
                            { text: 'Challenge 10 (Rev, Web)', link: '/'},
                        ]
                    },
                    { 
                        text: 'CDDC', 
                        collapsed: true,
                        items: [
                            { text: 'uboot (Pwn)', link: '/'},
                            { text: 'Looney Tunable (Pwn)', link: '/'},
                            { text: 'Escape Room (Pwn)', link: '/'},
                            { text: 'ropvm (Rev, Pwn)', link: '/'},
                        ]
                    },
                ]
            },
            {
                text: '2024',
                items: [
                    { 
                        text: 'ICC', 
                        collapsed: true,
                        items: []
                    },
                    { 
                        text: 'GeekCon', 
                        collapsed: true,
                        items: []
                    },
                    { 
                        text: 'ACSC', 
                        collapsed: true,
                        items: []
                    },
                    { 
                        // rev, mobile, finals rev/pwn chall
                        text: 'LakeCTF', 
                        collapsed: true,
                        items: []   
                    },
                ]
            }
        ],
        
        search: { provider: 'local' },
        siteTitle: 'Home',

        socialLinks: [
            { icon: 'github', link: 'https://github.com/goatmilkkk' },
            { icon: 'twitter', link: 'https://x.com/goatmilkkk' }
        ]
    }
})
