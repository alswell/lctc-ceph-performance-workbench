/**
 * Created by chenkang1 on 2017/6/30.
 */
import lodash from "lodash";
import basicTableModel from "./basic/basicTable.model";
import { parse } from "qs";

const model = lodash.cloneDeep(basicTableModel);

export default {
  namespace: "sysdata",
  subscriptions: {
    setup({ dispatch, history }) {
      history.listen(location => {
        let param = parse(window.location.search, {
          ignoreQueryPrefix: true
        });
        if (location.pathname.indexOf("sysdata") > -1) {
          dispatch({ type: "sysdata/setId", payload: param });
          if (Object.keys(param).length === 0) {
            dispatch({ type: "refresh" });
          }
        }
      });
    }
  },
  state: {
    ...model.state,
    modalVisible: false,
    batchModalVisible: false,
    createModalVisible: false
  },

  effects: {
    ...model.effects
  },

  reducers: {
    ...model.reducers,
    setId(state, { payload: param }) {
      return {
        ...state,
        caseid: param.caseid
      };
    }
  }
};
