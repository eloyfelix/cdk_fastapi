from jpype import startJVM, getDefaultJVMPath, JPackage, java


CDK_JARFILE_PATH = "/code/cdk.jar"
OPSIN_JARFILE_PATH = "/code/opsin.jar"
WURCS_JARFILE_PATH = "/code/MolWURCS.jar"


# Start java virtual machine
startJVM(
    getDefaultJVMPath(),
    f"-Djava.class.path={CDK_JARFILE_PATH}:{OPSIN_JARFILE_PATH}:{WURCS_JARFILE_PATH}",
    convertStrings=False,
)

cdk = JPackage("org").openscience.cdk
MDLV2000Reader = cdk.io.MDLV2000Reader
MDLV2000Writer = cdk.io.MDLV2000Writer
MDLV3000Reader = cdk.io.MDLV3000Reader
MDLV3000Writer = cdk.io.MDLV3000Writer
SmilesParser = cdk.smiles.SmilesParser
SmilesGenerator = cdk.smiles.SmilesGenerator
SilentChemObjectBuilder = cdk.silent.SilentChemObjectBuilder
StructureDiagramGenerator = cdk.layout.StructureDiagramGenerator
AtomContainer = cdk.AtomContainer
AtomContainerManipulator = cdk.tools.manipulator.AtomContainerManipulator
MolecularFormulaManipulator = cdk.tools.manipulator.MolecularFormulaManipulator
# CDKHydrogenAdder = cdk.tools.CDKHydrogenAdder
DepictionGenerator = cdk.depict.DepictionGenerator
Projection = cdk.stereo.Projection
StereoElementFactory = cdk.stereo.StereoElementFactory
StringReader = java.io.StringReader
StringWriter = java.io.StringWriter

opsin = JPackage("uk").ac.cam.ch.wwmm.opsin
NameToStructure = opsin.NameToStructure

glycoinfo = JPackage("org").glycoinfo
MoleculeToWURCSGraph = glycoinfo.MolWURCS.exchange.toWURCS.MoleculeToWURCSGraph
WURCSFactory = glycoinfo.WURCSFramework.util.WURCSFactory
WURCSGraph = glycoinfo.WURCSFramework.wurcs.graph.WURCSGraph


def read_mol(structure):
    if "V2000" in structure:
        mr = MDLV2000Reader(StringReader(structure))
        mol = mr.read(AtomContainer())
    elif "V3000" in structure:
        mr = MDLV3000Reader(StringReader(structure))
        mol = mr.read(AtomContainer())
    else:
        sp = SmilesParser(SilentChemObjectBuilder.getInstance())
        try:
            mol = sp.parseSmiles(structure)
            # generate 2D coordinates
            sdg = StructureDiagramGenerator()
            sdg.setMolecule(mol)
            sdg.generateCoordinates()
            mol = sdg.getMolecule()
        except:
            mol = None
    return mol

def addStereoelements(structure):
    mol = read_mol(structure)
    if mol:
        mol.setStereoElements(
            StereoElementFactory.using3DCoordinates(mol)
            .interpretProjections(Projection.Chair, Projection.Haworth)
            .createAll()
        )
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    else:
        smiles = None
    return smiles


def addHydrogens(structure):
    mol = read_mol(structure)
    if mol:
        AtomContainerManipulator.convertImplicitToExplicitHydrogens(mol)
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    else:
        smiles = None
    return smiles


def removeHydrogens(structure):
    mol = read_mol(structure)
    if mol:
        AtomContainerManipulator.suppressHydrogens(mol)
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    else:
        smiles = None
    return smiles


def smiles2molfile(structure):
    molfile = None
    mol = read_mol(structure)
    if mol:
        # generate 2D coordinates
        sdg = StructureDiagramGenerator()
        sdg.setMolecule(mol)
        sdg.generateCoordinates()
        mol = sdg.getMolecule()

        molfile = StringWriter()
        mw = MDLV2000Writer(molfile)
        mw.writeMolecule(mol)
    return molfile


def molfile2smiles(structure):
    smiles = None
    mol = read_mol(structure)
    if mol:
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    return smiles


def getDepiction(structure):
    svg = None
    mol = read_mol(structure)
    if mol:
        depiction = DepictionGenerator().withSize(50, 50).withFillToFit().withAtomColors().depict(mol)
        svg = depiction.toSvgStr()

    return svg

def calculateFormula(structure):
    mol_formula = None
    mol = read_mol(structure)
    if mol:
        # adder = CDKHydrogenAdder.getInstance(mol.getNewBuilder())
        # adder.addImplicitHydrogens(mol)
        AtomContainerManipulator.convertImplicitToExplicitHydrogens(mol)
        molecularFormula = MolecularFormulaManipulator.getMolecularFormula(mol)
        mol_formula = MolecularFormulaManipulator.getString(molecularFormula)
    return mol_formula

def name2structure(name):
    nts = NameToStructure.getInstance()
    try:
        smiles = nts.parseToSmiles(name)
    except:
        smiles = None
    return smiles

def molfile2wurcs(structure):
    wurcs = None
    mol = read_mol(structure)
    if mol:
        graphs = MoleculeToWURCSGraph().start(mol)
        factory = WURCSFactory(graphs[0])
        wurcs = factory.getWURCS()
    return wurcs
