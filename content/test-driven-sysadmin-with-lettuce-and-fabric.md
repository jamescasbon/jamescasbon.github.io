Title: Test Driven Sysadmin with Lettuce and Fabric
Date: 2012-02-15 10:20
Category: Python
Tags: python, devops
Slug: test-driven-sysadmin-with-lettuce-and-fabric
Author: James Casbon
Summary: Short version for index and feeds

I have been thinking about test driven sysadmin recently. We wouldn&rsquo;t want
to write code without tests, so we also shouldn&rsquo;t want to create
untestable pieces of infrastructure.

I think cucumber (or gherkin) could be a nice way of expressing policy:

    Feature: Mail
        In order to handle mail
     
        Scenario: Mail relay
            Given I am a production server
            And I am not a mail server 
            Then I should have postfix installed
            And I should have a mail relay to mail.example.org
     
        Scenario: Mail server
            Given I am a mail server
            Then I should have postfix installed 
            And postfix should be running 
            And I should be listening on port 25

Now, the idea is that the scenarios are skipped when the clauses in the
&lsquo;given&rsquo; part are not met. In this case I have defined two
scenarios: a mail server and a production server to relay via a mail host. When
I run this against a host, the given clauses work out which policies to test. I
needed to teach lettuce to have skippable scenarios. You can find a rough and
ready implementation of this on [my branch of
lettuce](https://github.com/jamescasbon/lettuce/tree/sysadmin). Now all that is
needed is to implement the steps to check those features (which is at the
bottom of this post). 

The nice part about this is I can write a fair amount of logic in python to
test the state of the system, but these can be calling out to fabric simple
shell calls. i.e. I don&rsquo;t need to install python onto to the system I
wish to test. Changes in policy can be tested site wide by testing a feature
against all hosts. I can also test the external view of the test machine from
my box by say, accessing a port or using an http get.

This is just the sketch of an idea: I need to write a command line tool to
handle the setup of of fabric hosts, and to allow multiple hosts to be tested
at once. I would also like to add a fix mode, whereby failing steps could call
out to the code that corrects a failing policy. Do you think this is a good way
to test a policy?

    :::python
    from lettuce import *
    from fabric import api
    from fabric.api import env
    import socket
     
    servers = {
            'xxx.local': {
                'ip': ' xxxx',
                'roles': ['production']
            }
    }
     
    # world is the lettuce singleton
    world.hostname = socket.gethostname()
    world.installed = {'postfix': False }
     
    # configure fabric to point at localhost
    # and to supress output
    env.host_string = 'localhost'
    env.warn_only = True
    import fabric.state
    for k in  fabric.state.output:
        fabric.state.output[k] = False
     
     
    @step('I am a (\w+) server')
    def has_a_role(step, role):
        hostname = api.run('hostname')
        return role in servers[hostname]['roles']
     
    @step('I am not a (\w+) server')
    def doesnt_have_a_role(step, role):
        return not has_a_role(step, role)
     
    @step('I should have (\w+) installed')
    def check_installed(step, package):
        # should call out to apt/rpm
        return world.installed.get(package, False)
     
    @step('I should have a mail relay to (\w+)')
    def check_mail_relay(step, package):
        result = api.run('grep foo /etc/passwd')
        assert result, 'relay not set up'
     
     
    @step('(\w+) should be running')
    def check_service_running(step, service):
        return True
     
    @step('I should be listening on port (\d+)')
    def check_service_running(step, port):
        return True
