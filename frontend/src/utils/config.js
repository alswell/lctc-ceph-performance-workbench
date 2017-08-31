const APIV1 = '/api/v1'
const APIV2 = '/api/v2'
const APINEW = '/apinew'

module.exports = {
  pageSize: 4,
  name: 'AntD Admin',
  prefix: 'antdAdmin',
  footerText: 'Lenovo LCTC  © 2017 zelin',
  logo: '/logo.png',
  iconFontCSS: '/iconfont.css',
  iconFontJS: '/iconfont.js',
  YQL: ['http://www.zuimeitianqi.com'],
  CORS: ['http://localhost:7000'],
  openPages: ['/login'],
  apiPrefix: '/api/v1',
  api: {
    userLogin: `${APIV1}/user/login`,
    userLogout: `${APIV1}/user/logout`,
    userInfo: `${APIV1}/userInfo`,
    users: `${APIV1}/users`,
    posts: `${APIV1}/posts`,
    user: `${APIV1}/user/:id`,
    dashboard: `${APIV1}/dashboard`,
    test: `${APIV1}/test`,
    v1test: `${APIV1}/test`,
    v2test: `${APIV2}/test`,
    newUser: `${APINEW}/users`,
  },
}
