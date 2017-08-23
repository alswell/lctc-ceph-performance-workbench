/**
 * Created by chenkang1 on 2017/6/30.
 */
import lodash from 'lodash'
import basicTableModel from './basic/basicTable.model'

const model = lodash.cloneDeep(basicTableModel)

export default {
  namespace: 'fiojobs',
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
  },
}
