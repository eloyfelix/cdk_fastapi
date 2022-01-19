from jpype import startJVM, getDefaultJVMPath, JPackage, java

CDK_JARFILE_PATH = f"/opt/conda/share/java/cdk.jar"

# Start java virtual machine
startJVM(
    getDefaultJVMPath(), f"-Djava.class.path={CDK_JARFILE_PATH}", convertStrings=False
)

cdk = JPackage("org").openscience.cdk

MDLV2000Reader = cdk.io.MDLV2000Reader
MDLV2000Writer = cdk.io.MDLV2000Writer
SmilesParser = cdk.smiles.SmilesParser
SmilesGenerator = cdk.smiles.SmilesGenerator
SilentChemObjectBuilder = cdk.silent.SilentChemObjectBuilder
StructureDiagramGenerator = cdk.layout.StructureDiagramGenerator
AtomContainer = cdk.AtomContainer
AtomContainerManipulator = cdk.tools.manipulator.AtomContainerManipulator
DepictionGenerator = cdk.depict.DepictionGenerator
Projection = cdk.stereo.Projection
StereoElementFactory = cdk.stereo.StereoElementFactory
StringReader = java.io.StringReader
StringWriter = java.io.StringWriter


def addStereoelements(smiles):
    sp = SmilesParser(SilentChemObjectBuilder.getInstance())
    try:
        mol = sp.parseSmiles(smiles)
    except:
        mol = None

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


def addHydrogens(smiles):
    sp = SmilesParser(SilentChemObjectBuilder.getInstance())
    try:
        mol = sp.parseSmiles(smiles)
    except:
        mol = None

    if mol:
        AtomContainerManipulator.convertImplicitToExplicitHydrogens(mol)
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    else:
        smiles = None
    return smiles


def removeHydrogens(smiles):
    sp = SmilesParser(SilentChemObjectBuilder.getInstance())
    try:
        mol = sp.parseSmiles(smiles)
    except:
        mol = None

    if mol:
        AtomContainerManipulator.suppressHydrogens(mol)
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    else:
        smiles = None
    return smiles


def smiles2molfile(smiles):
    molfile = None
    sp = SmilesParser(SilentChemObjectBuilder.getInstance())
    try:
        mol = sp.parseSmiles(smiles)
    except:
        mol = None

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


def molfile2smiles(molfile):
    smiles = None
    mr = MDLV2000Reader(StringReader(molfile))
    mol = mr.read(AtomContainer())

    if mol:
        sg = SmilesGenerator.absolute()
        smiles = sg.create(mol)
    return smiles


def depict(smiles):
    svg = None
    sp = SmilesParser(SilentChemObjectBuilder.getInstance())
    try:
        mol = sp.parseSmiles(smiles)
    except:
        mol = None

    if mol:
        # generate 2D coordinates
        sdg = StructureDiagramGenerator()
        sdg.setMolecule(mol)
        sdg.generateCoordinates()
        mol = sdg.getMolecule()

        depiction = DepictionGenerator().withAtomColors().depict(mol)
        svg = depiction.toSvgStr()
    return svg
