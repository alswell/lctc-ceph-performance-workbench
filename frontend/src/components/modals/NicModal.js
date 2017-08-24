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



class NicModal extends React.Component {
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
      url: `sarnic?caseid=${this.state.id}`,
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
    const NicLine = ({data}) => {
      const content = []
      let allnodes = []
      let allnetworks = []
      for (let j=0; j<data.length; j++) {
        allnodes.push(data[j].node)
      }
      for (let j=0; j<data.length; j++) {
        allnetworks.push(data[j].network)
      }
      let nodes = []
      let networks = []

      let n = allnodes.length
      for (let i=0; i<n; i++) {
        let j = i+1
        while (j<n) {
          if (allnodes[i] == allnodes[j]){
            for (let k=j; k+1<n; k++){
              allnodes[k] =  allnodes[k+1]
            }
            n = n-1
          }
          else{j++}
        }
      }
      for  (let i=0; i<n; i++) {
        nodes[i]=allnodes[i]
      }

      //console.log(allnetworks)
      let m = allnetworks.length
      for (let i=0; i<m; i++) {
        let j = i+1
        while (j<m) {
          if (allnetworks[i] == allnetworks[j]){
            for (let k=j; k+1<m; k++){
              allnetworks[k] =  allnetworks[k+1]
            }
            m = m-1
          }
          else{j++}
        }
      }
      for  (let i=0; i<m; i++) {
        networks[i]=allnetworks[i]
      }
      for (let i=0; i<nodes.length; i++) {
        for (let k=0; k<networks.length; k++) {
          const linedata = []
          for (let j=0; j<data.length; j++) {
            if (data[j].node == nodes[i]){
              if (data[j].network == networks[k]){linedata.push(data[j])}
            }
          }
          if (linedata.length > 0){
            content.push(<p>{nodes[i]} {networks[k]}</p>)
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
         <NicLine data={this.props.selectedItems.length==0 ? this.state.data : this.props.selectedItems}/>
        </Modal>
      </div>
    )
  }

}


NicModal.propTypes = {
  title: PropTypes.string,
  visible: PropTypes.boolean,
  onOk: PropTypes.function,
  onCancel: PropTypes.function,
  selectedItems: PropTypes.array,
  checkedItems: PropTypes.array,
}

export default NicModal
