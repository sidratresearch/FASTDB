function uniformSample(message, metadata) {
  const attrs = message.attributes || {};

  const diaSourceId = attrs.diaSource_diaSourceId
    ? parseInt(attrs.diaSource_diaSourceId)
    : null;

  return diaSourceId % 113 === 0 ? message : null;
}
