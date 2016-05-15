var React = require('react');
var ReactDOM = require('react-dom');
var io = require('socket.io-client');

var Panel = require('react-bootstrap').Panel;
var FormGroup = require('react-bootstrap').FormGroup;
var FormControl = require('react-bootstrap').FormControl;
var InputGroup = require('react-bootstrap').InputGroup;
var Button = require('react-bootstrap').Button;

var socket = io.connect('http://' + document.domain + ':' + location.port);

var Message = React.createClass({
  render: function() {

    return (
        <div className="message">
            <span><strong>{this.props.user}</strong> {this.props.text}</span> 
            <hr/>
        </div>
    );
  }
});

var MessageList = React.createClass({

  componentDidUpdate: function() {
    ReactDOM.findDOMNode(this).scrollTop = ReactDOM.findDOMNode(this).scrollHeight;
  },

  render() {
      return (
          <div className='messageList'>
            {
              this.props.messages.map(function(message, i) {
                return (
                    <Message key={i} user={message.user} text={message.text}/>
                );
              })
            }
          </div>
      );
  }
});

var MessageForm = React.createClass({

  getInitialState() {
      return {text: ''};
  },

  handleSubmit(e) {
      e.preventDefault();
      var message = {
          user : "You:",
          text : this.state.text
      }
      this.props.onMessageSubmit(message); 
      this.setState({ text: '' });
  },

  handleChange(e) {
      this.setState({ text : e.target.value });
  },

  render() {
      return(
          <div className='messageForm'>
            <form onSubmit={this.handleSubmit}>
              <FormGroup>
                <InputGroup>
                  <FormControl type="text" onChange={this.handleChange} value={this.state.text}/>
                  <InputGroup.Button>
                    <Button type="submit">Send</Button>
                  </InputGroup.Button>
                </InputGroup>
              </FormGroup>
            </form>
          </div>
      );
  }
});

var BotApp = React.createClass({
  getInitialState: function() {
    return {messages: [{user: 'FriendBot:', text: 'Hi I\'m FriendBot!'}]};
  },

  componentDidMount() {
    socket.on('msg:response', this.handleMessageReceive);
  },

  handleMessageReceive(message) {
    var {messages} = this.state;
    messages.push(message);
    this.setState({messages});
  },

  handleMessageSubmit(message) {
    var {messages} = this.state;
    messages.push(message);
    this.setState({messages});
    socket.emit('msg:send', message);
  },

  render: function() {
    var _MessageForm = ( <MessageForm onMessageSubmit={this.handleMessageSubmit}/> );

    return (
        <div className="mainContent">
          <div className="container">
            <Panel header="FriendBot Chat" footer={_MessageForm}>
              <MessageList messages={this.state.messages}/>
            </Panel>
          </div>
        </div>
    );
  }
});

ReactDOM.render(
    <BotApp/>,
    document.getElementById('container')
);
