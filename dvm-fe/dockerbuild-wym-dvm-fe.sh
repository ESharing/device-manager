docker rmi -f nexus.utstar.com/wym_dvm_fe:latest
#cp /var/jenkins_home/workspace/WBS_Controller/spn/karaf/target/spn-karaf-1.0.0.0.tar.gz ./
#tar -zvxf spn-karaf-1.0.0.0.tar.gz
#rm -rf spn-karaf-1.0.0.0/configuration/initial/
docker build -f Dockerfile -t nexus.utstar.com/wym_dvm_fe:latest .
docker login nexus.utstar.com -u admin -p admin
docker push nexus.utstar.com/wym_dvm_fe
