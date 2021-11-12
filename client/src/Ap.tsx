import React from 'react';

interface MyMessageProps {
  message: string;
}

const MyMessage = (props: MyMessageProps) => {
  const { message } = props;
  return <div>My message is: {message}</div>;
};

export default MyMessage;
