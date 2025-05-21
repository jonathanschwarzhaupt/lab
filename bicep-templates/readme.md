# Bicep

## Getting started with the Azure CLI

The azure-cli is installed in the environment using mise if you are using Devpods.

Run `az account list` to see a list of the subscriptions for the logged-in user. If an empty list `[]` appears in the terminal, it means you need to log in firs: `az login`

## Commands

some commands that  I found useful:

Set the default resource group: `az configure --default group="bicep-testing"` (I created the resource group in the portal previously)

Deploy the bicep template: `az deployment group create --name deploy01 --template-file bicep-templates/first-template/main.bicep`

Verify the deployment: `az deployment group list --output table`

Note: the `--output table` flag is a global flag meaning it can be applied on many commands

To delete the resources the deployment created, and while keeping the reource group alive, use:

`az deployment group show --name deploy01 --query "properties.outputResources[*].id" --output tsv | xargs -n 1 az resource delete --ids`

I can use `xargs` to pipe the multi-line output into the next command, in this case one-by-one. This allows me to check if a specific resource ID gives trouble in deleting it. An alternative would be to do `az resource delete --ids $(az deployment group show ...)`
