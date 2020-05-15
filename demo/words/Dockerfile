# BUILD
FROM openjdk:8u171-jdk-alpine as build
WORKDIR /home/lab
RUN MAVEN_VERSION=3.5.0 \
 && cd /usr/share \
 && wget http://archive.apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz -O - | tar xzf - \
 && mv /usr/share/apache-maven-$MAVEN_VERSION /usr/share/maven \
 && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn


COPY pom.xml .
RUN mvn verify -DskipTests --fail-never

COPY src ./src
RUN mvn verify

# RUN
FROM openjdk:8u171-jre
WORKDIR /app
COPY src/main/resources /app/resources
COPY --from=build /home/lab/target .

ENTRYPOINT ["java", "-jar", "/app/words.jar"]
EXPOSE 8080