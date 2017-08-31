import React from 'react'
import PropTypes from 'prop-types'
import { Router } from 'dva/router'
import App from './routes/app'

const registerModel = (app, model) => {
  if (!(app._models.filter(m => m.namespace === model.namespace).length === 1)) {
    app.model(model)
  }
}

const Routers = function ({ history, app }) {
  const routes = [
    {
      path: '/',
      component: App,
      getIndexRoute (nextState, cb) {
        require.ensure([], require => {
          registerModel(app, require('./models/fiojobs.model'))
          cb(null, { component: require('./routes/fiojobs/') })
        }, 'fiojobs')
      },
      childRoutes: [
        {
          path: 'dashboard',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/dashboard'))
              cb(null, require('./routes/dashboard/'))
            }, 'dashboard')
          },
        }, {
          path: 'user',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/user'))
              cb(null, require('./routes/user/'))
            }, 'user')
          },
        }, {
          path: 'user/:id',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/user/detail'))
              cb(null, require('./routes/user/detail/'))
            }, 'user-detail')
          },
        }, {
          path: 'login',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/login'))
              cb(null, require('./routes/login/'))
            }, 'login')
          },
        }, {
          path: 'request',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/request/'))
            }, 'request')
          },
        }, {
          path: 'UIElement/iconfont',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/UIElement/iconfont/'))
            }, 'UIElement-iconfont')
          },
        }, {
          path: 'UIElement/search',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/UIElement/search/'))
            }, 'UIElement-search')
          },
        }, {
          path: 'UIElement/dropOption',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/UIElement/dropOption/'))
            }, 'UIElement-dropOption')
          },
        }, {
          path: 'UIElement/layer',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/UIElement/layer/'))
            }, 'UIElement-layer')
          },
        }, {
          path: 'UIElement/dataTable',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/UIElement/dataTable/'))
            }, 'UIElement-dataTable')
          },
        }, {
          path: 'UIElement/editor',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/UIElement/editor/'))
            }, 'UIElement-editor')
          },
        }, {
          path: 'chart/lineChart',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/chart/lineChart/'))
            }, 'chart-lineChart')
          },
        }, {
          path: 'chart/barChart',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/chart/barChart/'))
            }, 'chart-barChart')
          },
        }, {
          path: 'chart/areaChart',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/chart/areaChart/'))
            }, 'chart-areaChart')
          },
        }, {
          path: 'post',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/post'))
              cb(null, require('./routes/post/'))
            }, 'post')
          },
        },
        {
          path: 'host',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/host.model'))
              cb(null, require('./routes/host/'))
            }, 'host')
          },
        },
        {
          path: "host/:id",
          getComponent(nextState, cb) {
            require.ensure(
              [],
              require => {
                registerModel(app, require("./models/host.model"));
                cb(null, require("./routes/host/detail.js"));
              },
              "host-detail"
            );
          }
        },
        {
          path: 'fiotest/:jobid',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/fiotest.model'))
              cb(null, require('./routes/fiotest/'))
            }, 'fiotest')
          },
        }, {
          path: 'fiotest',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/fiotest.model'))
              cb(null, require('./routes/fiotest/'))
            }, 'fiotest')
          },
        },
        {
          path: 'fiojobs',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/fiojobs.model'))
              cb(null, require('./routes/fiojobs/'))
            }, 'fiojobs')
          },
        },
        {
          path: 'deploy',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/deploy.model'))
              cb(null, require('./routes/deploy/'))
            }, 'deploy')
          },
        },
        {
          path: 'sysdata/:caseid',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/sysdata.model'))
              cb(null, require('./routes/sysdata/'))
            }, 'sysdata')
          },
        },{
          path: 'sysdata',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/sysdata.model'))
              cb(null, require('./routes/sysdata/'))
            }, 'sysdata')
          },
        },
        {
          path: 'sysinfo/:jobid',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/sysinfo.model'))
              cb(null, require('./routes/sysinfo/'))
            }, 'sysinfo')
          },
        },{
          path: 'sysinfo',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/sysinfo.model'))
              cb(null, require('./routes/sysinfo/'))
            }, 'sysinfo')
          },
        },
        {
          path: "cephconfig/:id",
          getComponent(nextState, cb) {
            require.ensure(
              [],
              require => {
                registerModel(app, require("./models/cephconfig.model"));
                cb(null, require("./routes/cephconfig/"));
              },
              "cephconfig"
            );
          }
        }, 
        {
          path: "cephconfig",
          getComponent(nextState, cb) {
            require.ensure(
              [],
              require => {
                registerModel(app, require("./models/cephconfig.model"));
                cb(null, require("./routes/cephconfig/"));
              },
              "cephconfig"
            );
          }
        }, {
          path: "perfdump/:id",
          getComponent(nextState, cb) {
            require.ensure(
              [],
              require => {
                registerModel(app, require("./models/perfdump.model"));
                cb(null, require("./routes/perfdump/"));
              },
              "perfdump"
            );
          }
        }, 
        {
          path: "perfdump",
          getComponent(nextState, cb) {
            require.ensure(
              [],
              require => {
                registerModel(app, require("./models/perfdump.model"));
                cb(null, require("./routes/perfdump/"));
              },
              "perfdump"
            );
          }
        }, {
          path: 'test',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              registerModel(app, require('./models/test'))
              cb(null, require('./routes/test/'))
            }, 'test')
          },
        },
        {
          path: '*',
          getComponent (nextState, cb) {
            require.ensure([], require => {
              cb(null, require('./routes/error/'))
            }, 'error')
          },
        },
      ],
    },
  ]

  return <Router history={history} routes={routes} />
}

Routers.propTypes = {
  history: PropTypes.object,
  app: PropTypes.object,
}

export default Routers
