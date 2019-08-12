from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group


class Groups(models.Model):
    groupid = models.AutoField(db_column='groupid', primary_key=True)
    groupname = models.TextField(db_column='groupname', verbose_name="Group Name")

    class Meta:
        db_table = 'groups'
        verbose_name = "Groups"

    def __str__(self):
        return self.groupname


class Customer(models.Model):
    custid = models.AutoField(db_column='custId', primary_key=True)  # Field name made lowercase.
    custname = models.TextField(db_column='custName', blank=True, null=True, verbose_name='Customer\'s Name')  # Field name made lowercase.
    custaddress = models.TextField(db_column='custAddress', blank=True, null=True, verbose_name='Customer\'s Addresss')  # Field name made lowercase.
    custcontact = models.CharField(db_column='custContact', max_length=50, blank=True, null=True, verbose_name='Phone Number(s)')  # Field name made lowercase.
    custemail = models.CharField(db_column='custEmail', max_length=140, blank=True, null=True, verbose_name='E-Mail ID')  # Field name made lowercase.
    YES = 'yes'
    NO = 'no'
    ACTIVE_CHOICE =  ((YES, 'Active'), (NO, 'Inactive'))
    custisactive = models.CharField(db_column='custIsActive', choices=ACTIVE_CHOICE, max_length=3, verbose_name='Customer\'s Status')  # Field name made lowercase.
    custgroup = models.ForeignKey(Groups, models.DO_NOTHING, db_column='custgroup', verbose_name="Customer Group" )

    class Meta:
        db_table = 'customer'
        verbose_name = 'Name of the Business/Firm/Entity'
        verbose_name_plural = 'Name of the Business/Firm/Entity'

    def __str__(self):
        return self.custname


class Domain(models.Model):
    domainid = models.AutoField(db_column='domainId', primary_key=True)  # Field name made lowercase.
    domainaddress = models.CharField(db_column='domainAddress', max_length=250, blank=True, null=True, verbose_name='Domain Address')  # Field name made lowercase.
    domainrefcustid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='domainRefCustId', blank=True, null=True, verbose_name='Domain Mapped to Customer ID')  # Field name made lowercase.

    class Meta:
        db_table = 'domain'
        verbose_name = "Domain List"

    def __str__(self):
        return str(self.domainaddress) + '  |   ' + str(self.domainrefcustid)

    def get_domainaddress(self):
        return str(self.domainaddress)


class Person(models.Model):
    personid = models.AutoField(db_column='personId', primary_key=True)  # Field name made lowercase.
    personname = models.CharField(db_column='personName', max_length=100, blank=True, null=True, verbose_name='Person\'s Name')  # Field name made lowercase.
    PERSON_CONTACT_TYPE = (('email', 'E-Mail Address'), ('phone', 'Phone/Mobile Number'))
    personcontacttype = models.CharField(db_column='personContactType', max_length=5, default='email', null=True, choices=PERSON_CONTACT_TYPE, verbose_name='Contact Type')  # Field name made lowercase.
    personcontact = models.CharField(db_column='personContact', max_length=100, blank=True, null=True, verbose_name='Contact Email/Phone')  # Field name made lowercase.
    YES = 'yes'
    NO = 'no'
    ACTIVE_CHOICE =  ((YES, 'Active'), (NO, 'Inactive'))
    personactive = models.CharField(db_column='personActive', max_length=3, choices=ACTIVE_CHOICE, verbose_name='Is person Active?')  # Field name made lowercase.
    personrefcustid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='personRefCustId', blank=True, null=True, verbose_name='Mapped to Customer ID')  # Field name made lowercase.

    class Meta:
        db_table = 'person'
        verbose_name = "Contact Detail of Person"

    def __str__(self):
        return str(self.personname) + '  |  ' + str(self.personcontact) + '  |  ' + str(self.personrefcustid)


class Workorder(models.Model):
    woid = models.AutoField(db_column='woId', primary_key=True)  # Field name made lowercase.
    refpersonid = models.ManyToManyField(Person, verbose_name="Multiple Reference", db_column='refPersonId')
    #refpersonid = models.ForeignKey(Person, models.DO_NOTHING, db_column='refPersonId', blank=True, null=True, verbose_name='Reference By Person ID')  # Field name made lowercase.
    refdomainid = models.ManyToManyField(Domain, verbose_name="Select Domains", db_column='refDomainId')
    #refdomainid = models.ForeignKey(Domain, models.DO_NOTHING, db_column='refDomainId', blank=True, null=True, verbose_name='Reference Domain ID')  # Field name made lowercase.
    jobdesc = models.TextField(db_column='jobDesc', blank=True, null=True, verbose_name='Description of Work')  # Field name made lowercase.
    PRIORITY_STATUS = (
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ('sos', 'SOS/Very Urgent')
    )
    wopriority = models.CharField(db_column='woPriority', max_length=15, blank=True, null=True, choices=PRIORITY_STATUS, verbose_name='Priority of the Work')  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='createdAt', default=timezone.now, verbose_name='Work Order Created At')  # Field name made lowercase.
    JOB_STATUS = (
        ('working', 'In Progress'),
        ('completed', 'Completed'),
        ('finished', 'Finished'),
        ('awaiting', 'Awaiting For Reply'),
        ('resolved', 'Resolved')
    )
    jobstatus = models.CharField(db_column='jobStatus', max_length=50, blank=True, null=True, choices=JOB_STATUS, verbose_name='Current Job Status')  # Field name made lowercase.
    statusupdatedat = models.DateTimeField(db_column='statusUpdatedAt', default=timezone.now, verbose_name='Status Update Date/Time')  # Field name made lowercase.
    WORK_TYPE = (
        ('paid', "Paid"),
        ('maintenance', 'Maintenance'),
        ('unpaid', 'Unpaid/Free Work'),
        ('amc', 'Annual Maintenance')
    )
    worktype = models.CharField(db_column='workType', default='amc', choices=WORK_TYPE, verbose_name="Work Type", max_length=15)
    eta = models.DateTimeField(db_column='etaForWorkOrder', default=timezone.now,verbose_name="Estimated Time to Complete")

    class Meta:
        db_table = 'workorder'
        verbose_name = "Work Order"
        ordering = ('-woid',)

    def __str__(self):
        converttext = "# {}".format(self.woid)
        return converttext

    def domain_list(self):
        return ", ".join([str(p.get_domainaddress()) for p in self.refdomainid.all()])

    def workorder_number_list(self):
        return '#'+str(self.woid)
    workorder_number_list.short_description = "#"

    def get_status(self):
        return self.jobstatus


class Updates(models.Model):
    updateid = models.AutoField(db_column='updateId', primary_key=True)  # Field name made lowercase.
    refwoid = models.ForeignKey('Workorder', models.DO_NOTHING, db_column='refWoId', blank=True, null=True, verbose_name="Reference to WorkOrder ID")  # Field name made lowercase.
    updatetext = models.TextField(db_column='updateText', blank=True, null=True, verbose_name="Update Note for Customer")  # Field name made lowercase.
    internalnote = models.TextField(db_column='internalNote', blank=True, null=True, verbose_name="Internal Note")  # Field name made lowercase.
    updateat = models.DateTimeField(db_column='updateAt', default=timezone.now, verbose_name="Updated At")  # Field name made lowercase.
    refdomainid = models.ForeignKey(Domain, models.DO_NOTHING, db_column='refDomainId', blank=True, null=True,
                                    verbose_name='Reference Domain ID')  # Field name made lowercase.

    class Meta:
        db_table = 'updates'
        verbose_name = "Work Order Update"

    def __str__(self):
        return str(self.refwoid) + '  |  ' + str(self.refdomainid)

    def work_order_status(self):
        return self.refwoid.get_status()


