package com.alert.service;

import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Sinks;
import reactor.core.publisher.Sinks.Many;

@Service
public class EmitService {

  // logger 정의
  private static final Logger logger = LoggerFactory.getLogger(EmitService.class);

  public void emitMessageToUser(Map<String, Many<String>> userSinks, String userSeq, String progress) {
    Sinks.Many<String> userSink = userSinks.get(userSeq);
    if (userSink != null) {
      userSink.tryEmitNext(progress);

      userSinks.remove(userSeq); // 연결 해제
      logger.info("파이프라인 연결 종료");
    }
  }


}