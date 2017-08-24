/**
 * Created by chenkang1 on 2017/7/2.
 */
import React from 'react'
import { Modal } from 'antd'
import PropTypes from 'prop-types'
import qs from 'qs'
import {
  Button,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Label,
  Card,
} from 'recharts'
import styles from './Container.less'
import {fetchAndNotification} from "../../services/restfulService";
//import Container from "../../routes/chart/lineChart/index"



class DiskModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: {},
      id: window.location.search ? qs.parse(window.location.search,{ignoreQueryPrefix:true}).caseid
        : ""
    }
  }

  componentDidMount() {
    this.fetchDetail()
  }

  fetchDetail = () => {
    fetchAndNotification({
      url: `iostat?caseid=${this.state.id}`,
      method: 'get',
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        data: result.data.data
      })
    })
  }

  render () {
    const DiskLine = ({data}) => {
      const content = []
      let allosds = []
      let alldisks = []
      for (let j=0; j<data.length; j++) {
        allosds.push(data[j].osdnum)
      }
      for (let j=0; j<data.length; j++) {
        alldisks.push(data[j].diskname)
      }
      let osds = []
      let disks = []

      let n = allosds.length
      for (let i=0; i<n; i++) {
        let j = i+1
        while (j<n) {
          if (allosds[i] == allosds[j]){
            for (let k=j; k+1<n; k++){
              allosds[k] =  allosds[k+1]
            }
            n = n-1
          }
          else{j++}
        }
      }
      for  (let i=0; i<n; i++) {
        osds[i]=allosds[i]
      }

      let m = alldisks.length
      for (let i=0; i<m; i++) {
        let j = i+1
        while (j<m) {
          if (alldisks[i] == alldisks[j]){
            for (let k=j; k+1<m; k++){
              alldisks[k] =  alldisks[k+1]
            }
            m = m-1
          }
          else{j++}
        }
      }
      for  (let i=0; i<m; i++) {
        disks[i]=alldisks[i]
      }
      
      for (let i=0; i<osds.length; i++) {
        for (let k=0; k<disks.length; k++) {
          const linedata = []
          for (let j=0; j<data.length; j++) {
            if (data[j].osdnum == osds[i]){
              if (data[j].diskname == disks[k]){linedata.push(data[j])}
            }
          }
          if (linedata.length > 0){
            content.push(<p>{osds[i]} {disks[k]}</p>)
            content.push(
              <SimpleLineChart data={linedata}/>
            )
          }
        } 
      }
      return (
        <div> {content}</div>
      )
    }

    const Container = ({ children, ratio = 5 / 2, minHeight = 250, maxHeight = 350 }) => <div className={styles.container} style={{ minHeight, maxHeight }}>
      <div style={{ marginTop: `${100 / ratio}%` || '100%' }}></div>
      <div className={styles.content} style={{ minHeight, maxHeight }}>
        <ResponsiveContainer>
          {children}
        </ResponsiveContainer>
      </div>
    </div>

    const SimpleLineChart = ({data}) => {
      const linecolor = ["#ffc658", "#82ca9d", "#8884d8", "#cc3300", "ff7300"]
      let content = []
      for (let i=0; i<this.props.checkedItems.length; i++) {
        let j = i
        if ( i >= linecolor.length){j = 0}
        content.push(
          <Line type="monotone" dataKey={this.props.checkedItems[i]} stroke={linecolor[j]}/>
        )
      }
      return (
        <Container>
          <LineChart data={data} margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}>
            <XAxis dataKey="time" />
            <YAxis type="number" unit="%"/>
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Legend />
            {content}
          </LineChart>
        </Container>
      )
    }

    return (
      <div>
        <Modal
          title={this.props.title}
          visible={this.props.visible}
          onCancel={this.props.onCancel}
          width={1000}
          footer={null}
        >
         <DiskLine data={this.props.selectedItems.length==0 ? this.state.data : this.props.selectedItems}/>
        </Modal>
      </div>
    )
  }

}


DiskModal.propTypes = {
  title: PropTypes.string,
  visible: PropTypes.boolean,
  onOk: PropTypes.function,
  onCancel: PropTypes.function,
  selectedItems: PropTypes.array,
  checkedItems: PropTypes.array,
}

export default DiskModal
