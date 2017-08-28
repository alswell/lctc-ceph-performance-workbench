/**
 * Created by chenkang1 on 2017/7/2.
 */
import React from 'react'
import { Modal } from 'antd'
import PropTypes from 'prop-types'
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
  BarChart,
  Bar,
} from 'recharts'
import styles from './Container.less'
import {fetchAndNotification} from "../../services/restfulService";
//import Container from "../../routes/chart/lineChart/index"



class FioJobsModal extends React.Component {
  // constructor (props) {
  //   super(props)
  // }
  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: {},
      id: this.props.selectedItems ? this.props.selectedItems.id : ""
    }
  }

  componentDidMount() {
    this.fetchDetail()
  }

  fetchDetail = () => {
    const jobids = []
    this.props.selectedItems.map((item) => (jobids.push(item.id)))

    fetchAndNotification({
      url: `fiotest`,
      method: 'get',
      params: {'jobid': jobids},
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        data: result.data
      })
    })
  }

  render () {
    const Container = ({ children, ratio = 5 / 2, minHeight = 250, maxHeight = 350 }) => (
      <div className={styles.container} style={{ minHeight, maxHeight }}>
        <div style={{ marginTop: `${100 / ratio}%` || '100%' }}></div>
        <div className={styles.content} style={{ minHeight, maxHeight }}>
          <ResponsiveContainer>
            {children}
          </ResponsiveContainer>
        </div>
      </div>
    )

    const JobLine = ({data, type}) => {
      const linecolor = ["#ffc658", "#82ca9d", "#8884d8", "#cc3300", "ff7300"]
      //const linecolor = ["#ffc658"]
      let content = []
      let jobids = []
      let jobnames = []
      this.props.selectedItems.map((item) => (jobids.push(item.id)))
      this.props.selectedItems.map((item) => (jobnames.push(item.name)))
      for (let i=0; i<jobids.length; i++) {
        let j = i
        if ( i >= linecolor.length){j = 0}
        content.push(
          <Bar dataKey={`${jobids[i]}${jobnames[i]}_${type}`} fill={linecolor[j]} />
        ) 
      }
      return (
      <Container>
        <BarChart data={data} margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
          }}>
          <XAxis dataKey="casename"/>
          <YAxis />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          {content}
        </BarChart>
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
          <JobLine data={this.state.data} type={this.props.type}/>
        </Modal>
      </div>
    )
    
  }

}


FioJobsModal.propTypes = {
  title: PropTypes.string,
  visible: PropTypes.boolean,
  onOk: PropTypes.function,
  onCancel: PropTypes.function,
  selectedItems: PropTypes.array,
  type: PropTypes.string,
}

export default FioJobsModal
