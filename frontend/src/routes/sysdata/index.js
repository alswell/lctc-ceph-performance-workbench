/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'dva'
import DataTable from '../../components/BasicTable/DataTable'
import { Modal, Row, Col, Card, Button, Tabs, Checkbox } from 'antd'
import { Link } from 'dva/router'
import DropOption from '../../components/DropOption/DropOption'
import MemModal from '../../components/modals/MemModal'
import CpuModal from '../../components/modals/CpuModal'
import NicModal from '../../components/modals/NicModal'
import DiskModal from '../../components/modals/DiskModal'
import { fetchAndNotification } from '../../services/restfulService'
import qs from 'qs'

const confirm = Modal.confirm
const TabPane = Tabs.TabPane;

class SysData extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      checkedItems: [],
      id: window.location.search ? qs.parse(window.location.search,{ignoreQueryPrefix:true}).caseid
        : ""
    }
  }

  componentDidMount () {

  }

  handleMenuClick = (record, e) => {
    if (e.key === '1') {
      let { dispatch } = this.props
      dispatch({
        type: 'sysdata/showModal',
        payload: {
          key: 'modalVisible',
        },

      })
    } else if (e.key === '2') {
      confirm({
        title: 'Are you sure delete this record?',
        onOk () {
          console.log(record)
        },
      })
    }
  };

  showModal = (key) => {
    let { dispatch } = this.props
    dispatch({
      type: 'sysdata/showModal',
      payload: {
        key,
      },
    })
  };

  refresh = () => {
    this.props.dispatch({ type: 'sysdata/refresh' })
  };

  init = () => {
    this.cputableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          sorter: true,
          width: 80,
        }, {
          title: '%usr',
          dataIndex: 'usr',
          key: 'usr',
        }, {
          title: '%nice',
          dataIndex: 'nice',
          key: 'nice',
        }, {
          title: '%sys',
          dataIndex: 'sys',
          key: 'sys',
        },
        {
          title: '%iowait',
          dataIndex: 'iowait',
          key: 'iowait',
        }, {
          title: '%steal',
          dataIndex: 'steal',
          key: 'steal',
        }, {
          title: '%irq',
          dataIndex: 'irq',
          key: 'irq',
        },
        {  
          title: '%soft',
          dataIndex: 'soft',
          key: 'soft',
        }, {
          title: '%guest',
          dataIndex: 'guest',
          key: 'guest',
        }, {
          title: '%gnice',
          dataIndex: 'gnice',
          key: 'gnice',
        }, {
          title: '%idle',
          dataIndex: 'idle',
          key: 'idle',
        }, 
      ],
      fetchData: {
        url: this.props.host.caseid ? `sarcpu/${this.props.host.caseid}/`:`sarcpu`,
        params: null,
      },
      errorMsg: 'get sar cpu table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.memtableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          sorter: true,
          width: 80,
        }, {
          title: 'kbmemfree',
          dataIndex: 'kbmemfree',
          key: 'kbmemfree',
        }, {
          title: 'kbmemused',
          dataIndex: 'kbmemused',
          key: 'kbmemused',
        }, {
          title: '%memused',
          dataIndex: 'memused',
          key: 'memused',
        },
        {
          title: 'kbbuffers',
          dataIndex: 'kbbuffers',
          key: 'kbbuffers',
        }, {
          title: 'kbcached',
          dataIndex: 'kbcached',
          key: 'kbcached',
        }, {
          title: 'kbcommit',
          dataIndex: 'kbcommit',
          key: 'kbcommit',
        },
        {  
          title: '%commit',
          dataIndex: 'commit',
          key: 'commit',
        }, {
          title: 'kbactive',
          dataIndex: 'kbactive',
          key: 'kbactive',
        }, {
          title: 'kbinact',
          dataIndex: 'kbinact',
          key: 'kbinact',
        }, {
          title: 'kbdirty',
          dataIndex: 'kbdirty',
          key: 'kbdirty',
        }, 
      ],
      fetchData: {
        url: this.props.host.caseid ? `sarmem/${this.props.host.caseid}/`:`sarmem`,
        params: null,
      },
      errorMsg: 'get sarmem table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.nictableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          sorter: true,
          width: 80,
        }, {
          title: 'Network',
          dataIndex: 'network',
          key: 'network',
          sorter: true,
          width: 120,
        }, {
          title: 'rxpck/s',
          dataIndex: 'rxpcks',
          key: 'rxpcks',
        }, {
          title: 'txpck/s',
          dataIndex: 'txpcks',
          key: 'txpcks',
        }, {
          title: 'rxkB/s',
          dataIndex: 'rxkBs',
          key: 'rxkBs',
        },
        {
          title: 'txkB/s',
          dataIndex: 'txkBs',
          key: 'txkBs',
        }, {
          title: 'rxcmp/s',
          dataIndex: 'rxcmps',
          key: 'rxcmps',
        }, {
          title: 'txcmp/s',
          dataIndex: 'txcmps',
          key: 'txcmps',
        },
        {  
          title: 'rxmcst/s',
          dataIndex: 'rxmcsts',
          key: 'rxmcsts',
        }, 
      ],
      fetchData: {
        url: this.props.host.caseid ? `sarnic/${this.props.host.caseid}/`:`sarnic`,
        params: null,
      },
      errorMsg: 'get sarnic table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.iostattableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Node',
          dataIndex: 'node',
          key: 'node',
          sorter: true,
          width: 80,
        }, {
          title: 'osd',
          dataIndex: 'osdnum',
          key: 'osdnum',
          sorter: true,
        }, {
          title: 'Disk',
          dataIndex: 'diskname',
          key: 'diskname',
          sorter: true,
        }, {
          title: 'rrqm/s',
          dataIndex: 'rrqms',
          key: 'rrqm/s',
        }, {
          title: 'wrqm/s',
          dataIndex: 'wrqms',
          key: 'wrqms',
        }, {
          title: 'r/s',
          dataIndex: 'rs',
          key: 'rs',
        },
        {
          title: 'w/s',
          dataIndex: 'ws',
          key: 'ws',
        }, {
          title: 'rMB/s',
          dataIndex: 'rMBs',
          key: 'rMBs',
        }, {
          title: 'wMB/s',
          dataIndex: 'wMBs',
          key: 'wMBs',
        }, {  
          title: 'avgrq-sz',
          dataIndex: 'avgrqsz',
          key: 'avgrqsz',
        }, {
          title: 'await',
          dataIndex: 'await',
          key: 'await',
        }, {
          title: 'r_await',
          dataIndex: 'r_await',
          key: 'r_await',
        }, {
          title: 'w_await',
          dataIndex: 'w_await',
          key: 'w_await',
        }, {
          title: 'svctm',
          dataIndex: 'svctm',
          key: 'svctm',
        }, {
          title: '%util',
          dataIndex: 'util',
          key: 'util',
        }, 
      ],
      fetchData: {
        url: this.props.host.caseid ? `iostat/${this.props.host.caseid}/`:`iostat`,
        params: null,
      },
      errorMsg: 'get iostat table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.cephstatustableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Start Time',
          dataIndex: 'time',
          key: 'time',
          sorter: true,
          width: 150,
        }, {
          title: 'Health',
          dataIndex: 'health_overall_status',
          key: 'health_overall_status',
        }, {
          title: 'Health Summary',
          dataIndex: 'health_summary',
          key: 'health_summary',
        }, {
          title: 'Health Detail',
          dataIndex: 'health_detail',
          key: 'health_detail',
        }, {
          title: 'fsid',
          dataIndex: 'fsid',
          key: 'fsid',
        }, {
          title: 'monmap_mons',
          dataIndex: 'monmap_mons',
          key: 'monmap_mons',
        },
        {
          title: 'osdmap_osdmap_num_osds',
          dataIndex: 'osdmap_osdmap_num_osds',
          key: 'osdmap_osdmap_num_osds',
        }, {
          title: 'osdmap_osdmap_num_up_osds',
          dataIndex: 'osdmap_osdmap_num_up_osds',
          key: 'osdmap_osdmap_num_up_osds',
        }, {
          title: 'osdmap_osdmap_num_in_osds',
          dataIndex: 'osdmap_osdmap_num_in_osds',
          key: 'osdmap_osdmap_num_in_osds',
        },
        {  
          title: 'pgmap_pgs_by_state',
          dataIndex: 'pgmap_pgs_by_state',
          key: 'pgmap_pgs_by_state',
        }, {
          title: 'pgmap_num_pgs',
          dataIndex: 'pgmap_num_pgs',
          key: 'pgmap_num_pgs',
        }, {
          title: 'pgmap_data_bytes',
          dataIndex: 'pgmap_data_bytes',
          key: 'pgmap_data_bytes',
        }, {
          title: 'pgmap_bytes_used',
          dataIndex: 'pgmap_bytes_used',
          key: 'pgmap_bytes_used',
        }, {
          title: 'pgmap_bytes_avail',
          dataIndex: 'pgmap_bytes_avail',
          key: 'pgmap_bytes_avail',
        }, {
          title: 'pgmap_bytes_total',
          dataIndex: 'pgmap_bytes_total',
          key: 'pgmap_bytes_total',
        },
      ],
      fetchData: {
        url: this.props.host.caseid ? `cephstatus/${this.props.host.caseid}/`:`cephstatus`,
        params: null,
      },
      errorMsg: 'get sarnic table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.cephinfotableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Monitor Number',
          dataIndex: 'monnum',
          key: 'monnum',
        }, {
          title: 'Node Number',
          dataIndex: 'nodenum',
          key: 'nodenum',
        }, {
          title: 'Version',
          dataIndex: 'version',
          key: 'version',
        }, {
          title: 'osd Number',
          dataIndex: 'osdnum',
          key: 'osdnum',
        }, {
          title: 'global raw used',
          dataIndex: 'globalrawused',
          key: 'globalrawused',
        }, 
      ],
      title: 'Ceph Info',
      fetchData: {
        url: this.props.host.caseid ? `cephinfo/${this.props.host.caseid}/`:`cephinfo`,
        params: null,
      },
      errorMsg: 'get cephinfo table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.poolinfotableDataProps = {
      columns: [
        {
          title: 'Case ID',
          dataIndex: 'caseid',
          key: 'caseid',
          width: 60,
          sorter: true,
        }, {
          title: 'Pool Name',
          dataIndex: 'name',
          key: 'name',
        }, {
          title: 'PG Number',
          dataIndex: 'pgnum',
          key: 'pgnum',
        }, {
          title: 'Size',
          dataIndex: 'size',
          key: 'size',
        }, 
      ],
      title: 'Pool Info',
      fetchData: {
        url: this.props.host.caseid ? `poolinfo/${this.props.host.caseid}/`:`poolinfo`,
        params: null,
      },
      errorMsg: 'get poolinfo table error',
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "sysdata/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    }

    this.batchModalProps = {
      visible: this.props.host.batchModalVisible,
      maskClosable: true,
      title: '',
      wrapClassName: 'vertical-center-modal',
      selectedItems: this.props.host.selectedItems,
      checkedItems: this.state.checkedItems,
      onCancel: () => {
        let { dispatch } = this.props
        dispatch({
          type: 'sysdata/hideModal',
          payload: {
            key: 'batchModalVisible',
          },
        })
      },
    }
  };

  onChange = (checkedValues) => {
    this.setState({
      checkedItems: checkedValues
    })
  };


  render () {
    this.init()

    return (
      <div className="content-inner">
        <Tabs type="card">
          <TabPane tab="cpu" key="1">
              <Checkbox.Group onChange={this.onChange}>
                <Row>
                  <Col span={2}><Checkbox value="usr">%usr</Checkbox></Col>
                  <Col span={2}><Checkbox value="nice">%nice</Checkbox></Col>
                  <Col span={2}><Checkbox value="sys">%sys</Checkbox></Col>
                  <Col span={2}><Checkbox value="iowait">%iowait</Checkbox></Col>
                  <Col span={2}><Checkbox value="steal">%steal</Checkbox></Col>
                  <Col span={2}><Checkbox value="irq">%irq</Checkbox></Col>
                  <Col span={2}><Checkbox value="soft">%soft</Checkbox></Col>
                  <Col span={2}><Checkbox value="guest">%guest</Checkbox></Col>
                  <Col span={2}><Checkbox value="gnice">%gnice</Checkbox></Col>
                  <Col span={2}><Checkbox value="idle">%idle</Checkbox></Col>
                </Row>
              </Checkbox.Group>
              <Button 
                type="primary"
                onClick={this.showModal.bind(this, 'batchModalVisible')}
                disabled={this.state.id ? false : this.props.host.selectedItems.length === 0}
              >Chart</Button>
            <DataTable
              {...this.cputableDataProps}
            />
            {this.props.host.batchModalVisible && <CpuModal {...this.batchModalProps} />}
          </TabPane>
          <TabPane tab="memory" key="2">
            <Checkbox.Group onChange={this.onChange}>
                <Row>
                  <Col span={2}><Checkbox value="kbmemfree">kbmemfree</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbmemused">kbmemused</Checkbox></Col>
                  <Col span={2}><Checkbox value="memused">%memused</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbbuffers">kbbuffers</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbcached">kbcached</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbcommit">kbcommit</Checkbox></Col>
                  <Col span={2}><Checkbox value="commit">%commit</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbactive">kbactive</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbinact">kbinact</Checkbox></Col>
                  <Col span={2}><Checkbox value="kbdirty">kbdirty</Checkbox></Col>
                </Row>
              </Checkbox.Group>
              <Button type="primary" onClick={this.showModal.bind(this, 'batchModalVisible')}
                disabled={this.state.id ? false : this.props.host.selectedItems.length === 0}
              >Chart</Button>  
            <DataTable
              {...this.memtableDataProps}
            />
            {this.props.host.batchModalVisible && <MemModal {...this.batchModalProps} />}
          </TabPane>
          <TabPane tab="network" key="3">
            <Checkbox.Group onChange={this.onChange}>
                <Row>
                  <Col span={2}><Checkbox value="rxpcks">rxpck/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="txpcks">txpck/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="rxkBs">rxkB/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="txkBs">txkB/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="rxcmps">rxcmp/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="txcmps">txcmp/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="rxmcsts">rxmcst/s</Checkbox></Col>
                </Row>
              </Checkbox.Group>
              <Button type="primary" onClick={this.showModal.bind(this, 'batchModalVisible')}
                disabled={this.state.id ? false : this.props.host.selectedItems.length === 0}
              >Chart</Button> 
            <DataTable
              {...this.nictableDataProps}
            />
            {this.props.host.batchModalVisible && <NicModal {...this.batchModalProps} />}
          </TabPane>
          <TabPane tab="disk" key="4">
            <Checkbox.Group onChange={this.onChange}>
                <Row>
                  <Col span={2}><Checkbox value="rrqms">rrqm/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="wrqms">wrqm/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="rs">r/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="ws">w/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="rMBs">rMB/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="wMBs">wMB/s</Checkbox></Col>
                  <Col span={2}><Checkbox value="avgrqsz">avgrq-sz</Checkbox></Col>
                  <Col span={2}><Checkbox value="await">await</Checkbox></Col>
                  <Col span={2}><Checkbox value="r_await">r_await</Checkbox></Col>
                  <Col span={2}><Checkbox value="w_await">w_await</Checkbox></Col>
                  <Col span={2}><Checkbox value="svctm">svctm</Checkbox></Col>
                  <Col span={2}><Checkbox value="util">%util</Checkbox></Col>
                </Row>
              </Checkbox.Group>
              <Button type="primary" onClick={this.showModal.bind(this, 'batchModalVisible')}
                disabled={this.state.id ? false : this.props.host.selectedItems.length === 0}
              >Chart</Button> 
            <DataTable
              {...this.iostattableDataProps}
            />
            {this.props.host.batchModalVisible && <DiskModal {...this.batchModalProps} />}
          </TabPane>
          <TabPane tab="Ceph status" key="5">
            <DataTable
              {...this.cephstatustableDataProps}
            />
          </TabPane>
           <TabPane tab="Ceph info" key="6">
            <DataTable
              {...this.cephinfotableDataProps}
            />
          </TabPane>
          <TabPane tab="Ceph Pool" key="7">
            <DataTable
              {...this.poolinfotableDataProps}
            />
          </TabPane>
        </Tabs>
      </div>
    )
  }
}


function mapStateToProps ({ sysdata }) {
  return {
    host:sysdata,
  }
}

SysData.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object,
}

export default connect(mapStateToProps)(SysData)

