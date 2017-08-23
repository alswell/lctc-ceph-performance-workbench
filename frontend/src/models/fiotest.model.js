/**
 * Created by chenkang1 on 2017/6/30.
 */
import lodash from 'lodash'
import basicTableModel from './basic/basicTable.model'
import { parse } from 'qs'

const model = lodash.cloneDeep(basicTableModel)

export default {
  namespace: 'fiotest',

  subscriptions: {
   setup ({ dispatch,history }) {
    
    history.listen(location => {
        // console.log(location)
        let param = parse(window.location.search,{
        ignoreQueryPrefix:true
      })

      dispatch({type:'setId',payload:param})
      })
      
      // console.log(location)
    },
    
  },
  state: {
    ...model.state,
    modalVisible: false,
    iopsModalVisible: false,
    latModalVisible: false,
    bwModalVisible: false,
    createModalVisible: false,
  },

  effects: {
    ...model.effects,
  },

  reducers: {
    ...model.reducers,

    setId(state,{payload:param}){
      return {
        ...state,
        jobid:param.jobid
      }
    }
  },
}
